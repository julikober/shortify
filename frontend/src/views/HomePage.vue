<template>
  <div class="home-container">
    <h1>Welcome to Shortify</h1>
    <p class="lead">Create and manage shortened URLs with ease</p>
    
    <div class="actions">
      <router-link v-if="!authStore.isAuthenticated" to="/login" class="btn btn-primary">
        Login to Start
      </router-link>
      <router-link v-else to="/dashboard" class="btn btn-primary">
        Go to Dashboard
      </router-link>
    </div>
    
    <div class="features">
      <div class="feature-card card">
        <h3>Easy URL Shortening</h3>
        <p>Create short links with just a few clicks</p>
      </div>
      
      <div class="feature-card card">
        <h3>Custom URLs</h3>
        <p>Create memorable custom short links</p>
      </div>
      
      <div class="feature-card card">
        <h3>Link Analytics</h3>
        <p>Track how many times your links are clicked</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
</script>

<style scoped>
.home-container {
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.lead {
  font-size: 1.25rem;
  color: #666;
  margin-bottom: 2rem;
}

.actions {
  margin-bottom: 3rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.feature-card {
  text-align: center;
  padding: 1.5rem;
}

.feature-card h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  color: #4285f4;
}

.feature-card p {
  margin: 0;
  color: #666;
}
</style>