import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import * as Audio from 'expo-av';

export default function VoiceEntryScreen() {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [recordings, setRecordings] = useState([
    { id: 1, date: '2024-01-14', duration: '3:45', transcription: 'Had a great day today. The meeting went well...' },
    { id: 2, date: '2024-01-12', duration: '2:30', transcription: 'Feeling stressed about the project deadline...' },
  ]);
  const [isSaving, setIsSaving] = useState(false);
  const recordingRef = useRef(null);

  const handleStartRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.status !== 'granted') {
        Alert.alert('Permission Required', 'Audio recording permission is required');
        return;
      }

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const recording = new Audio.Recording();
      await recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
      await recording.startAsync();

      recordingRef.current = recording;
      setIsRecording(true);
      setRecordingTime(0);

      const timer = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

      const originalTimer = timer;
      recordingRef.current.timerRef = originalTimer;
    } catch (error) {
      Alert.alert('Error', 'Failed to start recording: ' + error.message);
    }
  };

  const handleStopRecording = async () => {
    try {
      if (recordingRef.current) {
        await recordingRef.current.stopAndUnloadAsync();
        clearInterval(recordingRef.current.timerRef);

        setIsRecording(false);
        setIsSaving(true);

        // Simulate save delay
        setTimeout(() => {
          Alert.alert('Success', `Voice entry saved (${formatTime(recordingTime)})`);
          setRecordings([
            ...recordings,
            {
              id: Math.max(...recordings.map(r => r.id), 0) + 1,
              date: new Date().toLocaleDateString(),
              duration: formatTime(recordingTime),
              transcription: 'Recording in progress... (transcription pending)',
            },
          ]);
          setRecordingTime(0);
          setIsSaving(false);
        }, 2000);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to stop recording: ' + error.message);
      setIsSaving(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleDeleteRecording = (id) => {
    setRecordings(recordings.filter(r => r.id !== id));
    Alert.alert('Deleted', 'Recording removed');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.recordingSection}>
        <Text style={styles.title}>Voice Entry</Text>

        <View style={styles.recordingCard}>
          <Text style={styles.recordingLabel}>
            {isRecording ? 'Recording in progress...' : 'Ready to record'}
          </Text>

          <View style={styles.timerDisplay}>
            <Text style={styles.timerText}>{formatTime(recordingTime)}</Text>
          </View>

          <View style={styles.recordingButtons}>
            {!isRecording ? (
              <TouchableOpacity
                style={styles.recordButton}
                onPress={handleStartRecording}
              >
                <MaterialCommunityIcons name="microphone" size={32} color="#fff" />
                <Text style={styles.recordButtonText}>Start Recording</Text>
              </TouchableOpacity>
            ) : (
              <TouchableOpacity
                style={[styles.recordButton, styles.recordButtonStop]}
                onPress={handleStopRecording}
              >
                <MaterialCommunityIcons name="stop-circle" size={32} color="#fff" />
                <Text style={styles.recordButtonText}>Stop Recording</Text>
              </TouchableOpacity>
            )}
          </View>

          {isSaving && (
            <View style={styles.savingContainer}>
              <ActivityIndicator size="small" color="#57b8d9" />
              <Text style={styles.savingText}>Saving recording...</Text>
            </View>
          )}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Voice Entries</Text>
        {recordings.length > 0 ? (
          recordings.map((recording) => (
            <View key={recording.id} style={styles.recordingItem}>
              <View style={styles.recordingItemIcon}>
                <MaterialCommunityIcons name="microphone-outline" size={20} color="#57b8d9" />
              </View>
              <View style={styles.recordingItemContent}>
                <Text style={styles.recordingItemDate}>{recording.date}</Text>
                <Text style={styles.recordingItemTranscription} numberOfLines={2}>
                  {recording.transcription}
                </Text>
                <Text style={styles.recordingItemDuration}>{recording.duration}</Text>
              </View>
              <TouchableOpacity
                onPress={() => handleDeleteRecording(recording.id)}
              >
                <MaterialCommunityIcons name="delete" size={18} color="#f59e0b" />
              </TouchableOpacity>
            </View>
          ))
        ) : (
          <View style={styles.emptyState}>
            <MaterialCommunityIcons name="microphone-off" size={48} color="#ccc" />
            <Text style={styles.emptyText}>No voice entries yet</Text>
          </View>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Tips</Text>
        <View style={styles.tipBox}>
          <MaterialCommunityIcons name="lightbulb-outline" size={20} color="#f59e0b" />
          <Text style={styles.tipText}>
            Voice entries are automatically transcribed and saved to your journal.
          </Text>
        </View>
        <View style={styles.tipBox}>
          <MaterialCommunityIcons name="lightbulb-outline" size={20} color="#f59e0b" />
          <Text style={styles.tipText}>
            Speak naturally. There's no need to edit or be perfect!
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  recordingSection: {
    backgroundColor: '#fff',
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  recordingCard: {
    backgroundColor: 'linear-gradient(135deg, #57b8d9 0%, #3a8fa8 100%)',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    elevation: 4,
    shadowColor: '#57b8d9',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  recordingLabel: {
    fontSize: 16,
    color: '#999',
    marginBottom: 16,
    textAlign: 'center',
  },
  timerDisplay: {
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    borderRadius: 12,
    paddingVertical: 20,
    paddingHorizontal: 30,
    marginBottom: 24,
  },
  timerText: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    fontFamily: 'monospace',
  },
  recordingButtons: {
    width: '100%',
  },
  recordButton: {
    backgroundColor: '#10b981',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
  },
  recordButtonStop: {
    backgroundColor: '#ef4444',
  },
  recordButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  savingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 16,
  },
  savingText: {
    fontSize: 13,
    color: '#999',
  },
  section: {
    backgroundColor: '#fff',
    padding: 16,
    marginVertical: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  recordingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  recordingItemIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#e0f2fe',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  recordingItemContent: {
    flex: 1,
  },
  recordingItemDate: {
    fontSize: 12,
    color: '#999',
    marginBottom: 4,
  },
  recordingItemTranscription: {
    fontSize: 13,
    color: '#333',
    marginBottom: 4,
  },
  recordingItemDuration: {
    fontSize: 11,
    color: '#57b8d9',
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
    backgroundColor: '#f9f9f9',
    borderRadius: 12,
  },
  emptyText: {
    fontSize: 14,
    color: '#999',
    marginTop: 8,
  },
  tipBox: {
    backgroundColor: '#fffbeb',
    borderLeftWidth: 4,
    borderLeftColor: '#f59e0b',
    padding: 12,
    borderRadius: 8,
    flexDirection: 'row',
    gap: 12,
    marginBottom: 12,
  },
  tipText: {
    flex: 1,
    fontSize: 12,
    color: '#333',
  },
});
