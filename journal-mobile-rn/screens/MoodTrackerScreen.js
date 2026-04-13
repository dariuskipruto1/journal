import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function MoodTrackerScreen() {
  const [selectedMood, setSelectedMood] = useState(3);

  const moods = [
    { value: 1, emoji: '😢', label: 'Terrible', color: '#ef4444' },
    { value: 2, emoji: '😕', label: 'Bad', color: '#f59e0b' },
    { value: 3, emoji: '😐', label: 'Okay', color: '#f59e0b' },
    { value: 4, emoji: '😊', label: 'Good', color: '#10b981' },
    { value: 5, emoji: '😄', label: 'Great', color: '#10b981' },
  ];

  const handleMoodSelect = (mood) => {
    setSelectedMood(mood);
    Alert.alert('Mood Logged', `You're feeling ${moods[mood - 1].label}! Remember to write about it.`);
  };

  const stats = [
    { label: 'This Week Avg', value: '3.5', icon: 'calendar-week' },
    { label: 'This Month Avg', value: '3.8', icon: 'calendar-month' },
    { label: 'Current Streak', value: '12 days', icon: 'fire' },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.title}>How are you feeling today?</Text>
        <View style={styles.moodGrid}>
          {moods.map((mood) => (
            <TouchableOpacity
              key={mood.value}
              style={[
                styles.moodCard,
                selectedMood === mood.value && styles.moodCardSelected,
              ]}
              onPress={() => handleMoodSelect(mood.value)}
            >
              <Text style={styles.moodEmoji}>{mood.emoji}</Text>
              <Text style={styles.moodLabel}>{mood.label}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Statistics</Text>
        {stats.map((stat, idx) => (
          <View key={idx} style={styles.statRow}>
            <MaterialCommunityIcons name={stat.icon} size={20} color="#57b8d9" />
            <View style={styles.statContent}>
              <Text style={styles.statLabel}>{stat.label}</Text>
              <Text style={styles.statValue}>{stat.value}</Text>
            </View>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Mood Insights</Text>
        <View style={styles.insightBox}>
          <MaterialCommunityIcons name="lightbulb-outline" size={24} color="#f59e0b" />
          <Text style={styles.insightText}>
            Your mood is improving this month! Keep journaling to understand your emotions better.
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
  section: {
    backgroundColor: '#fff',
    padding: 16,
    marginVertical: 8,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  moodGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'wrap',
  },
  moodCard: {
    width: '18%',
    alignItems: 'center',
    padding: 12,
    borderRadius: 12,
    backgroundColor: '#f9f9f9',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  moodCardSelected: {
    borderColor: '#57b8d9',
    backgroundColor: '#e0f2fe',
  },
  moodEmoji: {
    fontSize: 28,
    marginBottom: 4,
  },
  moodLabel: {
    fontSize: 10,
    color: '#666',
    textAlign: 'center',
  },
  statRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  statContent: {
    marginLeft: 12,
    flex: 1,
  },
  statLabel: {
    fontSize: 12,
    color: '#999',
  },
  statValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginTop: 2,
  },
  insightBox: {
    backgroundColor: '#fffbeb',
    borderLeftWidth: 4,
    borderLeftColor: '#f59e0b',
    padding: 12,
    borderRadius: 8,
    flexDirection: 'row',
    alignItems: 'center',
  },
  insightText: {
    marginLeft: 12,
    fontSize: 13,
    color: '#333',
    flex: 1,
  },
});
