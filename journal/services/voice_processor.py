"""
Voice Entry Processing Module
Handles voice recording transcription and processing
"""

import os
import logging
from django.conf import settings
from django.core.files.base import ContentFile
from journal.models import VoiceEntry, Entry
import requests

logger = logging.getLogger(__name__)


class VoiceProcessor:
    """Process voice entries and transcribe audio"""
    
    @staticmethod
    def transcribe_audio(voice_entry: VoiceEntry, language: str = "en-US"):
        """
        Transcribe audio file using configured service (Google, Azure, or AWS)
        """
        try:
            transcription_service = settings.VOICE_ENTRY_CONFIG.get("TRANSCRIPTION_SERVICE", "google")
            
            if transcription_service == "google":
                return VoiceProcessor._transcribe_with_google(voice_entry, language)
            elif transcription_service == "azure":
                return VoiceProcessor._transcribe_with_azure(voice_entry, language)
            elif transcription_service == "aws":
                return VoiceProcessor._transcribe_with_aws(voice_entry, language)
            else:
                return None
        except Exception as e:
            logger.error(f"Transcription failed for voice entry {voice_entry.id}: {str(e)}")  # type: ignore
            voice_entry.transcription_status = "failed"
            voice_entry.save()
            return None

    @staticmethod
    def _transcribe_with_google(voice_entry: VoiceEntry, language: str):
        """Transcribe using Google Cloud Speech-to-Text"""
        try:
            from google.cloud import speech_v1  # type: ignore
            
            client = speech_v1.SpeechClient()  # type: ignore
            
            with open(voice_entry.audio_file.path, 'rb') as audio_file:
                content = audio_file.read()
            
            audio = speech_v1.RecognitionAudio(content=content)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                sample_rate_hertz=16000,
                language_code=language,
            )
            
            response = client.recognize(config=config, audio=audio)
            
            transcription = ""
            confidence_sum = 0
            
            for result in response.results:
                for alternative in result.alternatives:
                    transcription += alternative.transcript + " "
                    if alternative.confidence:
                        confidence_sum += alternative.confidence
            
            avg_confidence = confidence_sum / max(1, len(response.results))
            
            voice_entry.transcription = transcription.strip()
            voice_entry.confidence_score = avg_confidence
            voice_entry.transcription_status = "completed"
            voice_entry.save()
            
            return voice_entry.transcription
        except ImportError:
            logger.error("Google Cloud Speech library not installed")
            return None

    @staticmethod
    def _transcribe_with_azure(voice_entry: VoiceEntry, language: str):
        """Transcribe using Azure Speech Services"""
        try:
            import azure.cognitiveservices.speech as speechsdk  # type: ignore
            
            speech_config = speechsdk.SpeechConfig(  # type: ignore
                subscription=os.getenv("AZURE_SPEECH_KEY"),
                region=os.getenv("AZURE_SPEECH_REGION", "eastus")
            )
            speech_config.speech_recognition_language = language
            
            audio_config = speechsdk.audio.AudioConfig(filename=voice_entry.audio_file.path)
            recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
            
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedFromAudio:
                voice_entry.transcription = result.text
                voice_entry.confidence_score = 0.95  # Azure doesn't expose confidence easily
                voice_entry.transcription_status = "completed"
                voice_entry.save()
                return voice_entry.transcription
            else:
                voice_entry.transcription_status = "failed"
                voice_entry.save()
                return None
        except ImportError:
            logger.error("Azure Speech SDK not installed")
            return None

    @staticmethod
    def _transcribe_with_aws(voice_entry: VoiceEntry, language: str):
        """Transcribe using AWS Transcribe"""
        try:
            import boto3
            
            client = boto3.client('transcribe')
            
            s3_client = boto3.client('s3')
            bucket = settings.BACKUP_CONFIG["BACKUP_PROVIDERS"]["s3"]["aws_storage_bucket_name"]
            key = f"voice-entries/{voice_entry.id}/{voice_entry.audio_file.name}"  # type: ignore
            
            s3_client.upload_file(voice_entry.audio_file.path, bucket, key)
            
            job_name = f"transcription-{voice_entry.id}"  # type: ignore
            response = client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': f's3://{bucket}/{key}'},
                MediaFormat='mp3',
                LanguageCode=language.split('-')[0]  # Extract language code
            )
            
            # Store job name for async processing
            voice_entry.transcription = f"Transcription job: {job_name}"
            voice_entry.transcription_status = "pending"
            voice_entry.save()
            
            return None  # Will be updated when job completes
        except ImportError:
            logger.error("Boto3 not installed")
            return None

    @staticmethod
    def create_entry_from_voice(voice_entry: VoiceEntry, category: str = "", tags=None):
        """
        Create a journal entry from voice transcription
        """
        if not voice_entry.transcription or voice_entry.transcription_status != "completed":
            raise ValueError("Voice entry transcription must be completed")
        
        # Create title from first words of transcription
        title = " ".join(voice_entry.transcription.split()[:10])
        
        entry = Entry.objects.create(
            user=voice_entry.user,
            title=title or "Voice Entry",
            content=voice_entry.transcription,
            category=category or "Voice Notes",
        )
        
        if tags:
            entry.tags.set(tags)
        
        voice_entry.entry = entry
        voice_entry.save()
        
        return entry
