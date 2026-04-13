import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
  Linking,
  SafeAreaView,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SettingsScreen({ navigation }) {
  const [settings, setSettings] = useState({
    darkMode: false,
    notifications: true,
    emailReminders: true,
    backupData: true,
    analyticsTracking: false,
  });

  const [userInfo, setUserInfo] = useState({
    name: 'John Doe',
    email: 'john@example.com',
    joinDate: 'January 2024',
  });

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', onPress: () => {} },
        {
          text: 'Logout',
          onPress: async () => {
            try {
              await AsyncStorage.removeItem('token');
              await AsyncStorage.removeItem('user');
              navigation?.reset({
                index: 0,
                routes: [{ name: 'Login' }],
              });
            } catch (error) {
              Alert.alert('Error', 'Failed to logout');
            }
          },
          style: 'destructive',
        },
      ]
    );
  };

  const handleToggleSetting = (key) => {
    setSettings(prev => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const handleOpenLink = (url) => {
    Linking.openURL(url).catch(() => {
      Alert.alert('Error', 'Could not open link');
    });
  };

  const settingsList = [
    {
      title: 'Display',
      items: [
        {
          icon: 'moon',
          label: 'Dark Mode',
          value: settings.darkMode,
          key: 'darkMode',
          type: 'toggle',
        },
      ],
    },
    {
      title: 'Notifications',
      items: [
        {
          icon: 'bell',
          label: 'Enable Notifications',
          value: settings.notifications,
          key: 'notifications',
          type: 'toggle',
        },
        {
          icon: 'email',
          label: 'Email Reminders',
          value: settings.emailReminders,
          key: 'emailReminders',
          type: 'toggle',
        },
      ],
    },
    {
      title: 'Data & Privacy',
      items: [
        {
          icon: 'cloud-sync',
          label: 'Auto Backup',
          value: settings.backupData,
          key: 'backupData',
          type: 'toggle',
        },
        {
          icon: 'chart-line',
          label: 'Analytics Tracking',
          value: settings.analyticsTracking,
          key: 'analyticsTracking',
          type: 'toggle',
        },
      ],
    },
    {
      title: 'About',
      items: [
        {
          icon: 'information',
          label: 'App Version',
          value: '1.0.0',
          type: 'text',
        },
        {
          icon: 'file-document',
          label: 'Privacy Policy',
          type: 'link',
          url: 'https://journaldesk.io/privacy',
        },
        {
          icon: 'file-contract',
          label: 'Terms of Service',
          type: 'link',
          url: 'https://journaldesk.io/terms',
        },
      ],
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.header}>
          <Text style={styles.title}>Settings</Text>
        </View>

        <View style={styles.profileCard}>
          <View style={styles.profileAvatar}>
            <Text style={styles.avatarText}>
              {userInfo.name.split(' ').map(n => n[0]).join('')}
            </Text>
          </View>
          <View style={styles.profileInfo}>
            <Text style={styles.profileName}>{userInfo.name}</Text>
            <Text style={styles.profileEmail}>{userInfo.email}</Text>
            <Text style={styles.profileDate}>Joined {userInfo.joinDate}</Text>
          </View>
          <TouchableOpacity style={styles.editButton}>
            <MaterialCommunityIcons name="pencil" size={18} color="#57b8d9" />
          </TouchableOpacity>
        </View>

        {settingsList.map((section, idx) => (
          <View key={idx} style={styles.section}>
            <Text style={styles.sectionTitle}>{section.title}</Text>
            {section.items.map((item, itemIdx) => (
              <View key={itemIdx}>
                <View style={styles.settingRow}>
                  <View style={styles.settingLeft}>
                    <View style={styles.settingIcon}>
                      <MaterialCommunityIcons
                        name={item.icon}
                        size={20}
                        color="#57b8d9"
                      />
                    </View>
                    <Text style={styles.settingLabel}>{item.label}</Text>
                  </View>

                  {item.type === 'toggle' && (
                    <Switch
                      value={item.value}
                      onValueChange={() => handleToggleSetting(item.key)}
                      trackColor={{ false: '#d0d0d0', true: '#b3e5fc' }}
                      thumbColor={item.value ? '#57b8d9' : '#f0f0f0'}
                    />
                  )}

                  {item.type === 'text' && (
                    <Text style={styles.settingValue}>{item.value}</Text>
                  )}

                  {item.type === 'link' && (
                    <TouchableOpacity
                      onPress={() => handleOpenLink(item.url)}
                      style={styles.linkButton}
                    >
                      <MaterialCommunityIcons
                        name="open-in-new"
                        size={18}
                        color="#57b8d9"
                      />
                    </TouchableOpacity>
                  )}
                </View>
                {itemIdx < section.items.length - 1 && <View style={styles.divider} />}
              </View>
            ))}
          </View>
        ))}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Account</Text>
          <TouchableOpacity
            style={styles.dangerButton}
            onPress={handleLogout}
          >
            <MaterialCommunityIcons name="logout" size={20} color="#ef4444" />
            <Text style={styles.dangerButtonText}>Logout</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Journal Desk v1.0.0</Text>
          <Text style={styles.footerSubtext}>© 2024 Journal Desk Inc.</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
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
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  profileCard: {
    backgroundColor: '#fff',
    margin: 12,
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  profileAvatar: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#57b8d9',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  avatarText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  profileInfo: {
    flex: 1,
  },
  profileName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 2,
  },
  profileEmail: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  profileDate: {
    fontSize: 11,
    color: '#999',
  },
  editButton: {
    padding: 8,
  },
  section: {
    backgroundColor: '#fff',
    marginVertical: 8,
  },
  sectionTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#999',
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 8,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  settingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  settingIcon: {
    width: 36,
    height: 36,
    borderRadius: 8,
    backgroundColor: '#e0f2fe',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  settingLabel: {
    fontSize: 14,
    color: '#333',
    fontWeight: '500',
  },
  settingValue: {
    fontSize: 13,
    color: '#999',
  },
  linkButton: {
    padding: 8,
  },
  divider: {
    height: 1,
    backgroundColor: '#f0f0f0',
    marginHorizontal: 16,
  },
  dangerButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 12,
  },
  dangerButtonText: {
    fontSize: 14,
    color: '#ef4444',
    fontWeight: '600',
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  footerText: {
    fontSize: 12,
    color: '#999',
  },
  footerSubtext: {
    fontSize: 11,
    color: '#bbb',
    marginTop: 2,
  },
});
