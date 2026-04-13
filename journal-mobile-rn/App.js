import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { ActivityIndicator, View } from 'react-native';

// Screens
import LoginScreen from './screens/LoginScreen';
import SignupScreen from './screens/SignupScreen';
import DashboardScreen from './screens/DashboardScreen';
import EntriesScreen from './screens/EntriesScreen';
import CreateEntryScreen from './screens/CreateEntryScreen';
import MoodTrackerScreen from './screens/MoodTrackerScreen';
import AnalyticsScreen from './screens/AnalyticsScreen';
import TasksScreen from './screens/TasksScreen';
import VoiceEntryScreen from './screens/VoiceEntryScreen';
import NotificationsScreen from './screens/NotificationsScreen';
import SettingsScreen from './screens/SettingsScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const AuthStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerShown: false,
      animationEnabled: true,
    }}
  >
    <Stack.Screen 
      name="Login" 
      component={LoginScreen}
      options={{ animationEnabled: true }}
    />
    <Stack.Screen 
      name="Signup" 
      component={SignupScreen}
      options={{ animationTypeForReplace: true }}
    />
  </Stack.Navigator>
);

const HomeStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: '#57b8d9',
      },
      headerTintColor: '#fff',
      headerTitleStyle: {
        fontWeight: 'bold',
      },
      headerBackTitle: 'Back',
    }}
  >
    <Stack.Screen 
      name="DashboardHome" 
      component={DashboardScreen}
      options={{ 
        title: 'Dashboard',
        headerShown: true,
      }}
    />
    <Stack.Screen 
      name="CreateEntry" 
      component={CreateEntryScreen}
      options={{ title: 'New Entry' }}
    />
  </Stack.Navigator>
);

const EntriesStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: '#57b8d9',
      },
      headerTintColor: '#fff',
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }}
  >
    <Stack.Screen 
      name="EntriesList" 
      component={EntriesScreen}
      options={{ title: 'My Entries' }}
    />
    <Stack.Screen 
      name="CreateEntryFromList" 
      component={CreateEntryScreen}
      options={{ title: 'New Entry' }}
    />
  </Stack.Navigator>
);

const MoodStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: '#57b8d9',
      },
      headerTintColor: '#fff',
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }}
  >
    <Stack.Screen 
      name="MoodTrackerHome" 
      component={MoodTrackerScreen}
      options={{ title: 'Mood Tracker' }}
    />
  </Stack.Navigator>
);

const MoreStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: '#57b8d9',
      },
      headerTintColor: '#fff',
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }}
  >
    <Stack.Screen 
      name="Analytics" 
      component={AnalyticsScreen}
      options={{ title: 'Analytics' }}
    />
    <Stack.Screen 
      name="Tasks" 
      component={TasksScreen}
      options={{ title: 'Tasks' }}
    />
    <Stack.Screen 
      name="VoiceEntry" 
      component={VoiceEntryScreen}
      options={{ title: 'Voice Entry' }}
    />
    <Stack.Screen 
      name="Notifications" 
      component={NotificationsScreen}
      options={{ title: 'Notifications' }}
    />
    <Stack.Screen 
      name="Settings" 
      component={SettingsScreen}
      options={{ title: 'Settings' }}
    />
  </Stack.Navigator>
);

const AppStack = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      headerShown: false,
      tabBarIcon: ({ focused, color, size }) => {
        let iconName;
        if (route.name === 'Home') {
          iconName = focused ? 'home' : 'home-outline';
        } else if (route.name === 'Entries') {
          iconName = focused ? 'book' : 'book-outline';
        } else if (route.name === 'Mood') {
          iconName = focused ? 'emoticon-happy' : 'emoticon-neutral';
        } else if (route.name === 'More') {
          iconName = focused ? 'menu' : 'menu-outline';
        }
        return <MaterialCommunityIcons name={iconName} size={size} color={color} />;
      },
      tabBarActiveTintColor: '#57b8d9',
      tabBarInactiveTintColor: '#999',
      tabBarStyle: {
        backgroundColor: '#fff',
        borderTopColor: '#e0e0e0',
      },
    })}
  >
    <Tab.Screen 
      name="Home" 
      component={HomeStack}
      options={{ 
        title: 'Dashboard',
        tabBarLabel: 'Dashboard',
      }}
    />
    <Tab.Screen 
      name="Entries" 
      component={EntriesStack}
      options={{ 
        title: 'Entries',
        tabBarLabel: 'Entries',
      }}
    />
    <Tab.Screen 
      name="Mood" 
      component={MoodStack}
      options={{ 
        title: 'Mood',
        tabBarLabel: 'Mood',
      }}
    />
    <Tab.Screen 
      name="More" 
      component={MoreStack}
      options={{ 
        title: 'More',
        tabBarLabel: 'More',
      }}
    />
  </Tab.Navigator>
);

export default function App() {
  const [state, dispatch] = React.useReducer(
    (prevState, action) => {
      switch (action.type) {
        case 'RESTORE_TOKEN':
          return {
            ...prevState,
            isLoading: false,
            isSignout: false,
            userToken: action.payload,
          };
        case 'SIGN_IN':
          return {
            ...prevState,
            isSignout: false,
            userToken: action.payload,
          };
        case 'SIGN_OUT':
          return {
            ...prevState,
            isSignout: true,
            userToken: null,
          };
      }
    },
    {
      isLoading: true,
      isSignout: false,
      userToken: null,
    }
  );

  useEffect(() => {
    const bootstrapAsync = async () => {
      let userToken;
      try {
        userToken = await AsyncStorage.getItem('userToken');
      } catch (e) {
        console.error('Failed to restore token', e);
      }
      dispatch({ type: 'RESTORE_TOKEN', payload: userToken });
    };

    bootstrapAsync();
  }, []);

  if (state.isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' }}>
        <ActivityIndicator size="large" color="#57b8d9" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      {state.userToken == null ? <AuthStack /> : <AppStack />}
    </NavigationContainer>
  );
}
