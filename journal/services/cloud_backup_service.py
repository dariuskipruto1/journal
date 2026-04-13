"""
Cloud Backup Service
Handles backup and restore of user data to various providers
"""

import json
import logging
import zipfile
import io
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from journal.models import BackupData, Entry, DocumentUpload, UserPreferences

logger = logging.getLogger(__name__)


class CloudBackupService:
    """Service for managing cloud backups"""
    
    @staticmethod
    def create_backup(user, backup_type='manual', provider='local'):
        """
        Create a backup of user data
        """
        try:
            backup = BackupData.objects.create(
                user=user,
                backup_type=backup_type,
                backup_provider=provider,
                status='in_progress'
            )
            
            # Create backup data
            backup_data = CloudBackupService._prepare_backup_data(user)
            
            # Store based on provider
            if provider == 's3':
                location = CloudBackupService._backup_to_s3(user, backup, backup_data)
            elif provider == 'gcs':
                location = CloudBackupService._backup_to_gcs(user, backup, backup_data)
            else:  # local
                location = CloudBackupService._backup_locally(user, backup, backup_data)
            
            # Update backup record
            backup.backup_location = location
            backup.entries_count = Entry.objects.filter(user=user).count()
            backup.file_size = len(backup_data)
            backup.status = 'completed'
            backup.completed_at = timezone.now()
            backup.save()
            
            logger.info(f"Backup created for user {user.id} at {location}")
            return backup
            
        except Exception as e:
            logger.error(f"Backup creation failed for user {user.id}: {str(e)}")
            backup.status = 'failed'
            backup.error_message = str(e)
            backup.save()
            raise

    @staticmethod
    def _prepare_backup_data(user):
        """
        Prepare user data for backup (JSON format)
        """
        entries = Entry.objects.filter(user=user)
        documents = DocumentUpload.objects.filter(user=user)
        
        data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'backup_date': datetime.now().isoformat(),
            'entries': [],
            'documents': [],
        }
        
        # Include entries
        for entry in entries:
            entry_data = {
                'id': entry.id,  # type: ignore
                'title': entry.title,
                'content': entry.content,
                'category': entry.category,
                'mood': entry.mood,
                'is_starred': entry.is_starred,
                'task': entry.task,
                'task_priority': entry.task_priority,
                'task_completed': entry.task_completed,
                'created_at': entry.date_created.isoformat(),
                'updated_at': entry.date_updated.isoformat(),
                'tags': [tag.name for tag in entry.tags.all()]
            }
            data['entries'].append(entry_data)
        
        # Include document metadata
        for doc in documents:
            doc_data = {
                'id': doc.id,  # type: ignore
                'title': doc.title,
                'file_type': doc.file_type,
                'status': doc.status,
                'uploaded_at': doc.uploaded_at.isoformat(),
            }
            data['documents'].append(doc_data)
        
        return json.dumps(data, indent=2).encode('utf-8')

    @staticmethod
    def _backup_locally(user, backup: BackupData, data: bytes):
        """
        Save backup locally
        """
        import os
        backup_dir = settings.BASE_DIR / 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        filename = f"backup_{user.id}_{backup.id}.json"  # type: ignore
        filepath = backup_dir / filename
        
        with open(filepath, 'wb') as f:
            f.write(data)
        
        return str(filepath)

    @staticmethod
    def _backup_to_s3(user, backup: BackupData, data: bytes):
        """
        Upload backup to AWS S3
        """
        try:
            import boto3
            
            s3_config = settings.BACKUP_CONFIG['BACKUP_PROVIDERS']['s3']
            s3 = boto3.client(
                's3',
                aws_access_key_id=s3_config['aws_access_key_id'],
                aws_secret_access_key=s3_config['aws_secret_access_key'],
                region_name=s3_config['aws_s3_region_name']
            )
            
            bucket = s3_config['aws_storage_bucket_name']
            key = f"backups/{user.id}/backup_{backup.id}.json"  # type: ignore
            
            s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=data,
                ContentType='application/json'
            )
            
            return f"s3://{bucket}/{key}"
            
        except ImportError:
            logger.error("Boto3 not installed for S3 backup")
            raise
        except Exception as e:
            logger.error(f"S3 backup failed: {str(e)}")
            raise

    @staticmethod
    def _backup_to_gcs(user, backup: BackupData, data: bytes):
        """
        Upload backup to Google Cloud Storage
        """
        try:
            from google.cloud import storage
            
            gcs_config = settings.BACKUP_CONFIG['BACKUP_PROVIDERS']['gcs']
            client = storage.Client(project=gcs_config['project_id'])
            bucket = client.bucket(gcs_config['bucket_name'])
            
            blob = bucket.blob(f"backups/{user.id}/backup_{backup.id}.json")  # type: ignore
            blob.upload_from_string(data)
            
            return f"gs://{gcs_config['bucket_name']}/backups/{user.id}/backup_{backup.id}.json"  # type: ignore
            
        except ImportError:
            logger.error("Google Cloud Storage library not installed")
            raise
        except Exception as e:
            logger.error(f"GCS backup failed: {str(e)}")
            raise

    @staticmethod
    def restore_backup(user, backup: BackupData):
        """
        Restore user data from backup
        """
        try:
            # Load backup data
            if backup.backup_provider == 's3':
                data = CloudBackupService._restore_from_s3(backup)
            elif backup.backup_provider == 'gcs':
                data = CloudBackupService._restore_from_gcs(backup)
            else:
                data = CloudBackupService._restore_locally(backup)
            
            backup_json = json.loads(data.decode('utf-8'))
            
            # TODO: Implement restore logic (recreate entries, etc.)
            # This would involve creating new Entry records from backup data
            
            backup.restored_at = timezone.now()
            backup.save()
            
            logger.info(f"Backup restored for user {user.id}")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed for user {user.id}: {str(e)}")
            raise

    @staticmethod
    def _restore_locally(backup: BackupData):
        """Load local backup"""
        with open(backup.backup_location, 'rb') as f:
            return f.read()

    @staticmethod
    def _restore_from_s3(backup: BackupData):
        """Load backup from S3"""
        try:
            import boto3
            
            s3_config = settings.BACKUP_CONFIG['BACKUP_PROVIDERS']['s3']
            s3 = boto3.client(
                's3',
                aws_access_key_id=s3_config['aws_access_key_id'],
                aws_secret_access_key=s3_config['aws_secret_access_key'],
            )
            
            # Parse S3 location
            parts = backup.backup_location.replace('s3://', '').split('/', 1)
            bucket = parts[0]
            key = parts[1]
            
            response = s3.get_object(Bucket=bucket, Key=key)
            return response['Body'].read()
            
        except Exception as e:
            logger.error(f"S3 restore failed: {str(e)}")
            raise

    @staticmethod
    def _restore_from_gcs(backup: BackupData):
        """Load backup from GCS"""
        try:
            from google.cloud import storage
            
            gcs_config = settings.BACKUP_CONFIG['BACKUP_PROVIDERS']['gcs']
            client = storage.Client(project=gcs_config['project_id'])
            
            # Parse GCS location
            parts = backup.backup_location.replace('gs://', '').split('/', 1)
            bucket_name = parts[0]
            key = parts[1]
            
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(key)
            return blob.download_as_bytes()
            
        except Exception as e:
            logger.error(f"GCS restore failed: {str(e)}")
            raise

    @staticmethod
    def _delete_from_s3(backup: BackupData):
        """Delete backup from AWS S3"""
        try:
            import boto3
            
            s3_config = settings.BACKUP_CONFIG['BACKUP_PROVIDERS']['s3']
            s3 = boto3.client(
                's3',
                aws_access_key_id=s3_config['aws_access_key_id'],
                aws_secret_access_key=s3_config['aws_secret_access_key'],
                region_name=s3_config['aws_s3_region_name']
            )
            
            # Parse S3 location
            parts = backup.backup_location.replace('s3://', '').split('/', 1)
            bucket = parts[0]
            key = parts[1]
            
            s3.delete_object(Bucket=bucket, Key=key)
            logger.info(f"Deleted backup from S3: {backup.backup_location}")
        except Exception as e:
            logger.error(f"Failed to delete S3 backup: {str(e)}")

    @staticmethod
    def _delete_from_gcs(backup: BackupData):
        """Delete backup from Google Cloud Storage"""
        try:
            from google.cloud import storage
            
            gcs_config = settings.BACKUP_CONFIG['BACKUP_PROVIDERS']['gcs']
            client = storage.Client(project=gcs_config['project_id'])
            
            # Parse GCS location
            parts = backup.backup_location.replace('gs://', '').split('/', 1)
            bucket_name = parts[0]
            key = parts[1]
            
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(key)
            blob.delete()
            logger.info(f"Deleted backup from GCS: {backup.backup_location}")
        except Exception as e:
            logger.error(f"Failed to delete GCS backup: {str(e)}")

    @staticmethod
    def delete_old_backups(user, keep_count=10):
        """
        Delete old backups, keeping only the most recent
        """
        backups = BackupData.objects.filter(
            user=user,
            status='completed'
        ).order_by('-created_at')[keep_count:]
        
        for backup in backups:
            try:
                # Delete from provider
                if backup.backup_provider == 's3':
                    CloudBackupService._delete_from_s3(backup)
                elif backup.backup_provider == 'gcs':
                    CloudBackupService._delete_from_gcs(backup)
                else:
                    import os
                    if os.path.exists(backup.backup_location):
                        os.remove(backup.backup_location)
                
                # Delete record
                backup.delete()
            except Exception as e:
                logger.error(f"Failed to delete backup {backup.id}: {str(e)}")  # type: ignore
