import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';
import router from '../router';

export const useAuthStore = defineStore('auth', () => {
  const access_token = ref(localStorage.getItem('token') || null);
  const expires_in = ref(null);
  const loading = ref(false);
  const error = ref('');

  const isAuthenticated = computed(() => !!access_token.value);

  async function login(username, password) {
    loading.value = true;
    error.value = '';
    
    try {
      const response = await axios.post('/auth/login', 
        new URLSearchParams({
          username: username,
          password: password
        }), 
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );
      
      access_token.value = response.data.access_token;
      expires_in.value = response.data.expires_in;
      
      // Store token in localStorage for persistence
      localStorage.setItem('token', access_token.value);
      
      // Set axios default auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token.value}`;
      
      return response;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed';
      throw new Error(error.value);
    } finally {
      loading.value = false;
    }
  }

  function logout() {
    // Call logout API (optional, depends on your backend implementation)
    axios.post('/auth/logout')
      .catch(err => console.error('Logout error:', err))
      .finally(() => {
        // Clear token and state regardless of API success
        access_token.value = null;
        expires_in.value = null;
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
        router.push('/login');
      });
  }

  // Initialize auth header if token exists
  if (access_token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token.value}`;
  }

  return {
    access_token,
    isAuthenticated,
    loading,
    error,
    login,
    logout
  };
});