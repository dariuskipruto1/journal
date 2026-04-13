import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { BarChart, LineChart, PieChart } from 'react-native-chart-kit';

const screenWidth = Dimensions.get('window').width;

export default function AnalyticsScreen() {
  const [timeRange, setTimeRange] = useState('week');

  const weeklyData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        data: [2, 3, 2, 4, 5, 3, 4],
      },
    ],
  };

  const moodData = {
    labels: ['Great', 'Good', 'Okay', 'Bad'],
    datasets: [
      {
        data: [25, 30, 28, 17],
      },
    ],
  };

  const moodPieData = [
    { name: 'Great', population: 25, color: '#10b981', legendFontColor: '#333' },
    { name: 'Good', population: 30, color: '#57b8d9', legendFontColor: '#333' },
    { name: 'Okay', population: 28, color: '#f59e0b', legendFontColor: '#333' },
    { name: 'Bad', population: 17, color: '#ef4444', legendFontColor: '#333' },
  ];

  const stats = [
    { label: 'Total Entries', value: '156', icon: 'file-document', color: '#57b8d9' },
    { label: 'Avg Mood', value: '3.8/5', icon: 'emoticon-happy', color: '#10b981' },
    { label: 'Streak', value: '12 days', icon: 'fire', color: '#f59e0b' },
    { label: 'Words Written', value: '12.5K', icon: 'text-box', color: '#7c5dcd' },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.title}>Analytics</Text>
        <View style={styles.timeRangeButtons}>
          {['week', 'month', 'year'].map((range) => (
            <TouchableOpacity
              key={range}
              style={[
                styles.timeButton,
                timeRange === range && styles.timeButtonActive,
              ]}
              onPress={() => setTimeRange(range)}
            >
              <Text
                style={[
                  styles.timeButtonText,
                  timeRange === range && styles.timeButtonTextActive,
                ]}
              >
                {range.charAt(0).toUpperCase() + range.slice(1)}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Key Metrics</Text>
        <View style={styles.statsGrid}>
          {stats.map((stat, idx) => (
            <View key={idx} style={styles.statCard}>
              <View style={[styles.statIcon, { backgroundColor: stat.color + '20' }]}>
                <MaterialCommunityIcons name={stat.icon} size={24} color={stat.color} />
              </View>
              <Text style={styles.statValue}>{stat.value}</Text>
              <Text style={styles.statLabel}>{stat.label}</Text>
            </View>
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Entries Per Day</Text>
        <BarChart
          data={weeklyData}
          width={screenWidth - 32}
          height={220}
          yAxisLabel=""
          chartConfig={{
            backgroundColor: '#fff',
            backgroundGradientFrom: '#fff',
            backgroundGradientTo: '#fff',
            decimalPlaces: 0,
            color: (opacity = 1) => `rgba(87, 184, 217, ${opacity})`,
            labelColor: (opacity = 1) => `rgba(51, 51, 51, ${opacity})`,
            style: {
              borderRadius: 6,
            },
            propsForBackgroundLines: {
              strokeDasharray: '',
            },
          }}
          style={{ borderRadius: 6 }}
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Mood Distribution</Text>
        <PieChart
          data={moodPieData}
          width={screenWidth - 32}
          height={220}
          chartConfig={{
            backgroundColor: '#fff',
            backgroundGradientFrom: '#fff',
            backgroundGradientTo: '#fff',
            color: (opacity = 1) => `rgba(51, 51, 51, ${opacity})`,
          }}
          accessor="population"
          backgroundColor="transparent"
          paddingLeft="15"
          center={[0, 0]}
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Productivity Score</Text>
        <View style={styles.scoreCard}>
          <View style={styles.scoreCircle}>
            <Text style={styles.scoreValue}>78%</Text>
            <Text style={styles.scoreLabel}>This Month</Text>
          </View>
          <View style={styles.scoreDetails}>
            <View style={styles.scoreRow}>
              <MaterialCommunityIcons name="check-circle" size={20} color="#10b981" />
              <Text style={styles.scoreRowText}>Regular journaling</Text>
            </View>
            <View style={styles.scoreRow}>
              <MaterialCommunityIcons name="check-circle" size={20} color="#10b981" />
              <Text style={styles.scoreRowText}>Consistent mood tracking</Text>
            </View>
            <View style={styles.scoreRow}>
              <MaterialCommunityIcons name="alert-circle" size={20} color="#f59e0b" />
              <Text style={styles.scoreRowText}>Voice entries could improve</Text>
            </View>
          </View>
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
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  timeRangeButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  timeButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  timeButtonActive: {
    backgroundColor: '#57b8d9',
  },
  timeButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#999',
  },
  timeButtonTextActive: {
    color: '#fff',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  statCard: {
    width: '48%',
    backgroundColor: '#f9f9f9',
    padding: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  statIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    color: '#999',
  },
  scoreCard: {
    backgroundColor: '#f9f9f9',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  scoreCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#57b8d9',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  scoreValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  scoreLabel: {
    fontSize: 11,
    color: '#fff',
    marginTop: 2,
  },
  scoreDetails: {
    flex: 1,
  },
  scoreRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  scoreRowText: {
    marginLeft: 8,
    fontSize: 12,
    color: '#333',
  },
});
