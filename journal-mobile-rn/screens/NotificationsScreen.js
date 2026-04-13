import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  FlatList,
  Alert,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function NotificationsScreen() {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'reminder',
      title: 'Time to journal',
      message: 'You have not journaled today. Write something!',
      timestamp: '10:30 AM',
      icon: 'bell',
      color: '#57b8d9',
      read: false,
    },
    {
      id: 2,
      type: 'mood',
      title: 'Mood tracking',
      message: 'Don\'t forget to log your mood for today',
      timestamp: '9:15 AM',
      icon: 'emoticon-happy',
      color: '#10b981',
      read: false,
    },
    {
      id: 3,
      type: 'backup',
      title: 'Cloud backup completed',
      message: 'Your entries have been backed up successfully',
      timestamp: 'Yesterday',
      icon: 'cloud-check',
      color: '#7c5dcd',
      read: true,
    },
    {
      id: 4,
      type: 'milestone',
      title: 'Milestone reached!',
      message: 'You\'ve written 100 entries!',
      timestamp: '3 days ago',
      icon: 'trophy',
      color: '#f59e0b',
      read: true,
    },
    {
      id: 5,
      type: 'reminder',
      title: 'Weekly summary ready',
      message: 'Check your weekly insights and analytics',
      timestamp: '1 week ago',
      icon: 'chart-box',
      color: '#57b8d9',
      read: true,
    },
  ]);

  const [filter, setFilter] = useState('all');

  const handleMarkAsRead = (id) => {
    setNotifications(notifications.map(notif =>
      notif.id === id ? { ...notif, read: true } : notif
    ));
  };

  const handleDeleteNotification = (id) => {
    setNotifications(notifications.filter(notif => notif.id !== id));
  };

  const handleMarkAllAsRead = () => {
    setNotifications(notifications.map(notif => ({ ...notif, read: true })));
    Alert.alert('Done', 'All notifications marked as read');
  };

  const handleClearAll = () => {
    Alert.alert(
      'Clear All Notifications',
      'Are you sure you want to delete all notifications?',
      [
        { text: 'Cancel', onPress: () => {} },
        {
          text: 'Delete',
          onPress: () => {
            setNotifications([]);
          },
          style: 'destructive',
        },
      ]
    );
  };

  const filteredNotifications = notifications.filter(notif => {
    if (filter === 'unread') return !notif.read;
    if (filter === 'read') return notif.read;
    return true;
  });

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Notifications</Text>
        {unreadCount > 0 && (
          <View style={styles.badge}>
            <Text style={styles.badgeText}>{unreadCount}</Text>
          </View>
        )}
      </View>

      {notifications.length > 0 && (
        <View style={styles.actions}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={handleMarkAllAsRead}
          >
            <MaterialCommunityIcons name="check-all" size={16} color="#57b8d9" />
            <Text style={styles.actionText}>Mark All as Read</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={handleClearAll}
          >
            <MaterialCommunityIcons name="delete-outline" size={16} color="#ef4444" />
            <Text style={[styles.actionText, { color: '#ef4444' }]}>Clear All</Text>
          </TouchableOpacity>
        </View>
      )}

      <View style={styles.filterButtons}>
        {['all', 'unread', 'read'].map((filterType) => (
          <TouchableOpacity
            key={filterType}
            style={[
              styles.filterButton,
              filter === filterType && styles.filterButtonActive,
            ]}
            onPress={() => setFilter(filterType)}
          >
            <Text
              style={[
                styles.filterButtonText,
                filter === filterType && styles.filterButtonTextActive,
              ]}
            >
              {filterType === 'all' ? 'All' : filterType.charAt(0).toUpperCase() + filterType.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <ScrollView style={styles.notificationsList}>
        {filteredNotifications.length > 0 ? (
          filteredNotifications.map((notification) => (
            <View
              key={notification.id}
              style={[
                styles.notificationCard,
                !notification.read && styles.notificationCardUnread,
              ]}
            >
              <View
                style={[
                  styles.notificationIcon,
                  { backgroundColor: notification.color + '20' },
                ]}
              >
                <MaterialCommunityIcons
                  name={notification.icon}
                  size={24}
                  color={notification.color}
                />
              </View>

              <View style={styles.notificationContent}>
                <Text style={styles.notificationTitle}>{notification.title}</Text>
                <Text style={styles.notificationMessage} numberOfLines={2}>
                  {notification.message}
                </Text>
                <Text style={styles.notificationTime}>{notification.timestamp}</Text>
              </View>

              <TouchableOpacity
                style={styles.notificationAction}
                onPress={() => {
                  if (!notification.read) {
                    handleMarkAsRead(notification.id);
                  } else {
                    handleDeleteNotification(notification.id);
                  }
                }}
              >
                {!notification.read ? (
                  <MaterialCommunityIcons name="check" size={20} color="#57b8d9" />
                ) : (
                  <MaterialCommunityIcons name="delete" size={20} color="#f59e0b" />
                )}
              </TouchableOpacity>
            </View>
          ))
        ) : (
          <View style={styles.emptyState}>
            <MaterialCommunityIcons name="bell-outline" size={48} color="#ccc" />
            <Text style={styles.emptyText}>
              {filter === 'unread'
                ? 'No unread notifications'
                : filter === 'read'
                  ? 'No read notifications'
                  : 'No notifications yet'}
            </Text>
            <Text style={styles.emptySubtext}>
              You're all caught up!
            </Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#fff',
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  badge: {
    backgroundColor: '#ef4444',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    minWidth: 24,
    alignItems: 'center',
  },
  badgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  actions: {
    backgroundColor: '#fff',
    paddingHorizontal: 16,
    paddingVertical: 12,
    flexDirection: 'row',
    gap: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: '#f9f9f9',
  },
  actionText: {
    fontSize: 12,
    color: '#57b8d9',
    fontWeight: '600',
  },
  filterButtons: {
    backgroundColor: '#fff',
    paddingHorizontal: 16,
    paddingVertical: 12,
    flexDirection: 'row',
    gap: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  filterButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  filterButtonActive: {
    backgroundColor: '#57b8d9',
  },
  filterButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#999',
  },
  filterButtonTextActive: {
    color: '#fff',
  },
  notificationsList: {
    paddingHorizontal: 8,
    paddingVertical: 8,
  },
  notificationCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    marginVertical: 6,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    borderLeftWidth: 4,
    borderLeftColor: 'transparent',
  },
  notificationCardUnread: {
    backgroundColor: '#f0f7ff',
    borderLeftColor: '#57b8d9',
  },
  notificationIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notificationContent: {
    flex: 1,
  },
  notificationTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 2,
  },
  notificationMessage: {
    fontSize: 12,
    color: '#666',
    marginBottom: 6,
  },
  notificationTime: {
    fontSize: 10,
    color: '#999',
  },
  notificationAction: {
    padding: 8,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
    marginTop: 16,
    fontWeight: '500',
  },
  emptySubtext: {
    fontSize: 12,
    color: '#bbb',
    marginTop: 4,
  },
});
