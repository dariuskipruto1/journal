import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'http://journaldesk.example.com/api';

export default function DashboardScreen({ navigation }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    fetchDashboardData();
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      const user = await AsyncStorage.getItem('userData');
      if (user) {
        setUserData(JSON.parse(user));
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const token = await AsyncStorage.getItem('userToken');
      const response = await axios.get(`${API_BASE_URL}/stats/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchDashboardData();
    setRefreshing(false);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#57b8d9" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      {/* Welcome Section */}
      <View style={styles.welcomeSection}>
        <Text style={styles.welcomeTitle}>
          👋 Welcome back{userData?.first_name ? `, ${userData.first_name}` : ''}!
        </Text>
        <Text style={styles.welcomeSubtitle}>
          You're making progress on your journaling journey
        </Text>
      </View>

      {/* Stats Grid */}
      <View style={styles.statsGrid}>
        <View style={[styles.statCard, styles.statCardGreen]}>
          <MaterialCommunityIcons name="book-multiple" size={24} color="#fff" />
          <Text style={styles.statValue}>{stats?.total_entries || 0}</Text>
          <Text style={styles.statLabel}>Total Entries</Text>
        </View>

        <View style={[styles.statCard, styles.statCardBlue]}>
          <MaterialCommunityIcons name="calendar-week" size={24} color="#fff" />
          <Text style={styles.statValue}>{stats?.week_entries || 0}</Text>
          <Text style={styles.statLabel}>This Week</Text>
        </View>

        <View style={[styles.statCard, styles.statCardPurple]}>
          <MaterialCommunityIcons name="checkbox-marked-circle" size={24} color="#fff" />
          <Text style={styles.statValue}>{stats?.pending_tasks || 0}</Text>
          <Text style={styles.statLabel}>Pending Tasks</Text>
        </View>

        <View style={[styles.statCard, styles.statCardOrange]}>
          <MaterialCommunityIcons name="emoticon-happy" size={24} color="#fff" />
          <Text style={styles.statValue}>{stats?.avg_mood || '-'}</Text>
          <Text style={styles.statLabel}>Avg. Mood</Text>
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📝 Quick Actions</Text>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('CreateEntry')}
        >
          <MaterialCommunityIcons name="pencil-plus" size={20} color="#57b8d9" />
          <Text style={styles.actionButtonText}>New Entry</Text>
          <MaterialCommunityIcons name="chevron-right" size={20} color="#ccc" />
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('More', { screen: 'VoiceEntry' })}
        >
          <MaterialCommunityIcons name="microphone" size={20} color="#7c5dcd" />
          <Text style={styles.actionButtonText}>Voice Entry</Text>
          <MaterialCommunityIcons name="chevron-right" size={20} color="#ccc" />
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => navigation.navigate('Mood')}
        >
          <MaterialCommunityIcons name="emoticon-happy-outline" size={20} color="#f59e0b" />
          <Text style={styles.actionButtonText}>Log Mood</Text>
          <MaterialCommunityIcons name="chevron-right" size={20} color="#ccc" />
        </TouchableOpacity>
      </View>

      {/* Insights */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>✨ Insights</Text>
        <View style={styles.insightCard}>
          <Text style={styles.insightLabel}>🏆 Streak</Text>
          <Text style={styles.insightValue}>{stats?.current_streak || 0} days</Text>
          <Text style={styles.insightSubtext}>Keep it going!</Text>
        </View>
        <View style={styles.insightCard}>
          <Text style={styles.insightLabel}>📈 Productivity</Text>
          <Text style={styles.insightValue}>{stats?.productivity_score || 0}%</Text>
          <Text style={styles.insightSubtext}>This month</Text>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  welcomeSection: {
    backgroundColor: '#57b8d9',
    padding: 20,
    paddingTop: 10,
  },
  welcomeTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  welcomeSubtitle: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
  },
  statsGrid: {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 10,
    justifyContent: 'space-between',
  },
  statCard: {
    width: '48%',
    borderRadius: 12,
    padding: 16,
    marginBottom: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  statCardGreen: { backgroundColor: '#10b981' },
  statCardBlue: { backgroundColor: '#3b82f6' },
  statCardPurple: { backgroundColor: '#7c5dcd' },
  statCardOrange: { backgroundColor: '#f59e0b' },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginVertical: 4,
  },
  statLabel: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.9)',
    textAlign: 'center',
  },
  section: {
    backgroundColor: '#fff',
    marginVertical: 8,
    paddingVertical: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    paddingHorizontal: 16,
    marginBottom: 12,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  actionButtonText: {
    flex: 1,
    fontSize: 15,
    color: '#333',
    marginLeft: 12,
    fontWeight: '500',
  },
  insightCard: {
    marginHorizontal: 16,
    marginBottom: 10,
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#57b8d9',
  },
  insightLabel: {
    fontSize: 12,
    color: '#999',
    marginBottom: 4,
  },
  insightValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  insightSubtext: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
  },
});
