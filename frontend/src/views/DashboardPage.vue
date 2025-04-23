<template>
  <div>
    <h1>Dashboard</h1>
    
    <!-- Create New Link -->
    <div class="card create-link-section">
      <h2>Create New Short Link</h2>
      <div v-if="error" class="error-message">{{ error }}</div>
      
      <form @submit.prevent="createLink">
        <div class="form-group">
          <label for="url">URL to Shorten</label>
          <input 
            type="url" 
            id="url" 
            v-model="newUrl" 
            placeholder="https://example.com" 
            required
          />
        </div>
        
        <div class="form-group">
          <label for="customId">Custom ID (Optional)</label>
          <input 
            type="text" 
            id="customId" 
            v-model="customId" 
            placeholder="e.g., my-link"
          />
        </div>
        
        <button 
          type="submit" 
          class="btn btn-primary"
          :disabled="isCreating"
        >
          {{ isCreating ? 'Creating...' : 'Create Short Link' }}
        </button>
      </form>
    </div>
    
    <!-- Links List -->
    <div class="links-section">
      <h2>Your Links</h2>
      
      <div v-if="isLoading" class="loading">Loading your links...</div>
      
      <div v-else-if="!links.length" class="empty-state">
        You haven't created any links yet.
      </div>
      
      <div v-else class="links-list">
        <div v-for="link in links" :key="link.id" class="link-card card">
          <div class="link-info">
            <div class="short-url">{{ baseUrl }}{{ link.short_url }}</div>
            <div class="original-url">{{ link.url }}</div>
            <div class="link-stats">
              Clicks: {{ link.access_count }} | 
              Created: {{ formatDate(link.create_time) }}
            </div>
          </div>
          
          <div class="link-actions">
            <button @click="copyLink(baseUrl + link.short_url)" class="btn btn-primary">
              Copy
            </button>
            <button @click="deleteLink(link.id)" class="btn btn-danger">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useLinksStore } from '@/stores/links';

const linksStore = useLinksStore();
const links = ref([]);
const newUrl = ref('');
const customId = ref('');
const error = ref('');
const isLoading = ref(true);
const isCreating = ref(false);
const baseUrl = 'http://localhost:8000/api';

// Fetch links on component mount
onMounted(async () => {
  try {
    await fetchLinks();
  } catch (err) {
    error.value = 'Failed to load links';
  }
});

// Fetch links from the API
const fetchLinks = async () => {
  isLoading.value = true;
  try {
    const response = await linksStore.fetchLinks();
    links.value = response || [];
  } catch (err) {
    console.error('Error fetching links:', err);
    error.value = 'Failed to load links';
  } finally {
    isLoading.value = false;
  }
};

// Create a new short link
const createLink = async () => {
  if (!newUrl.value) {
    error.value = 'Please enter a URL';
    return;
  }
  
  error.value = '';
  isCreating.value = true;
  
  try {
    await linksStore.createLink(newUrl.value, customId.value || null);
    newUrl.value = '';
    customId.value = '';
    await fetchLinks();
  } catch (err) {
    error.value = err.message || 'Failed to create link';
  } finally {
    isCreating.value = false;
  }
};

// Delete a link
const deleteLink = async (id) => {
  if (!confirm('Are you sure you want to delete this link?')) {
    return;
  }
  
  try {
    await linksStore.deleteLink(id);
    await fetchLinks();
  } catch (err) {
    error.value = 'Failed to delete link';
  }
};

// Copy link to clipboard
const copyLink = (text) => {
  navigator.clipboard.writeText(text)
    .then(() => {
      alert('Link copied to clipboard!');
    })
    .catch(err => {
      console.error('Failed to copy link:', err);
      error.value = 'Failed to copy link';
    });
};

// Format date
const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString();
};
</script>

<style scoped>
h1 {
  margin-bottom: 1.5rem;
}

h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.create-link-section {
  margin-bottom: 2rem;
}

.links-section {
  margin-top: 2rem;
}

.links-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.link-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.short-url {
  font-weight: bold;
  color: #4285f4;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.original-url {
  color: #666;
  margin-bottom: 0.25rem;
  word-break: break-all;
}

.link-stats {
  font-size: 0.85rem;
  color: #888;
}

.link-actions {
  display: flex;
  gap: 0.5rem;
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
</style>