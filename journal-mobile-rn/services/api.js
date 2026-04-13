import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Change this to your actual backend URL
// For local development: 'http://192.168.1.X:8000/api' (use your machine's local IP)
// For production: 'https://yourdomain.com/api'
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - user should login again
      AsyncStorage.removeItem('token');
      AsyncStorage.removeItem('user');
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (username, password) => {
    try {
      const response = await apiClient.post('/auth/login/', { username, password });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  register: async (firstName, lastName, email, username, password) => {
    try {
      const response = await apiClient.post('/auth/register/', {
        first_name: firstName,
        last_name: lastName,
        email,
        username,
        password,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  logout: async () => {
    try {
      await apiClient.post('/auth/logout/');
      await AsyncStorage.removeItem('token');
      await AsyncStorage.removeItem('user');
    } catch (error) {
      // Even if logout fails, clear local storage
      await AsyncStorage.removeItem('token');
      await AsyncStorage.removeItem('user');
    }
  },
};

export const entriesAPI = {
  getAll: async (limit = 20, offset = 0) => {
    try {
      const response = await apiClient.get('/entries/', {
        params: { limit, offset },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getById: async (id) => {
    try {
      const response = await apiClient.get(`/entries/${id}/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  create: async (title, content, mood = 3, category = null) => {
    try {
      const response = await apiClient.post('/entries/', {
        title,
        content,
        mood,
        category,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  update: async (id, title, content, mood = 3, category = null) => {
    try {
      const response = await apiClient.patch(`/entries/${id}/`, {
        title,
        content,
        mood,
        category,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  delete: async (id) => {
    try {
      await apiClient.delete(`/entries/${id}/`);
    } catch (error) {
      throw error;
    }
  },

  toggleStar: async (id) => {
    try {
      const response = await apiClient.post(`/entries/${id}/toggle-star/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  search: async (query, limit = 20) => {
    try {
      const response = await apiClient.get('/entries/search/', {
        params: { q: query, limit },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export const statsAPI = {
  getDashboard: async () => {
    try {
      const response = await apiClient.get('/stats/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getMoodTrends: async (days = 7) => {
    try {
      const response = await apiClient.get('/stats/mood-trends/', {
        params: { days },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getProductivity: async () => {
    try {
      const response = await apiClient.get('/stats/productivity/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getStreak: async () => {
    try {
      const response = await apiClient.get('/stats/streak/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export const tasksAPI = {
  getAll: async () => {
    try {
      const response = await apiClient.get('/tasks/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  create: async (title, priority = 'medium', dueDate = null) => {
    try {
      const response = await apiClient.post('/tasks/', {
        title,
        priority,
        due_date: dueDate,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  toggle: async (id) => {
    try {
      const response = await apiClient.post(`/tasks/${id}/toggle/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  delete: async (id) => {
    try {
      await apiClient.delete(`/tasks/${id}/`);
    } catch (error) {
      throw error;
    }
  },
};

export const voiceAPI = {
  upload: async (audioFile, transcription = '') => {
    try {
      const formData = new FormData();
      formData.append('audio_file', {
        uri: audioFile,
        name: 'voice_entry.m4a',
        type: 'audio/m4a',
      });
      formData.append('transcription', transcription);

      const response = await apiClient.post('/voice-entries/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getAll: async () => {
    try {
      const response = await apiClient.get('/voice-entries/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  delete: async (id) => {
    try {
      await apiClient.delete(`/voice-entries/${id}/`);
    } catch (error) {
      throw error;
    }
  },
};

export const notificationsAPI = {
  getAll: async () => {
    try {
      const response = await apiClient.get('/notifications/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  markAsRead: async (id) => {
    try {
      const response = await apiClient.post(`/notifications/${id}/mark-read/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  delete: async (id) => {
    try {
      await apiClient.delete(`/notifications/${id}/`);
    } catch (error) {
      throw error;
    }
  },
};

export const userAPI = {
  getProfile: async () => {
    try {
      const response = await apiClient.get('/user/profile/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  updateProfile: async (firstName, lastName, email) => {
    try {
      const response = await apiClient.patch('/user/profile/', {
        first_name: firstName,
        last_name: lastName,
        email,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  updatePreferences: async (preferences) => {
    try {
      const response = await apiClient.patch('/user/preferences/', preferences);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default apiClient;
