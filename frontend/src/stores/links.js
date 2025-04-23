import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';

export const useLinksStore = defineStore('links', () => {
  const links = ref([]);
  const loading = ref(false);
  const error = ref('');

  async function fetchLinks() {
    loading.value = true;
    error.value = '';
    
    try {
      const response = await axios.get('/links');
      links.value = response.data;
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch links';
      console.error('Error fetching links:', err);
      throw new Error(error.value);
    } finally {
      loading.value = false;
    }
  }

  async function createLink(url, customId = null) {
    loading.value = true;
    error.value = '';
    
    try {
      let endpoint = `/links?url=${encodeURIComponent(url)}`;
      if (customId) {
        endpoint += `&custom_id=${encodeURIComponent(customId)}`;
      }
      
      const response = await axios.post(endpoint);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create link';
      throw new Error(error.value);
    } finally {
      loading.value = false;
    }
  }

  async function deleteLink(id) {
    loading.value = true;
    error.value = '';
    
    try {
      await axios.delete(`/links/${id}`);
      return true;
    } catch (err) {
      error.value = 'Failed to delete link';
      throw new Error(error.value);
    } finally {
      loading.value = false;
    }
  }

  async function getLinkAnalytics(id) {
    loading.value = true;
    error.value = '';
    
    try {
      const response = await axios.get(`/links/${id}/analytics`);
      return response.data;
    } catch (err) {
      error.value = 'Failed to fetch link analytics';
      throw new Error(error.value);
    } finally {
      loading.value = false;
    }
  }

  return {
    links,
    loading,
    error,
    fetchLinks,
    createLink,
    deleteLink,
    getLinkAnalytics
  };
});