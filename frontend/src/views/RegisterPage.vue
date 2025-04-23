<template>
  <div class="register-container">
    <div class="card">
      <h1>Create Account</h1>
      <div v-if="error" class="error-message">{{ error }}</div>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required
            autocomplete="username"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
            autocomplete="new-password"
          />
        </div>
        
        <div class="form-group">
          <label for="birthday">Birthday</label>
          <input 
            type="date" 
            id="birthday" 
            v-model="birthday" 
            required
          />
        </div>
        
        <button 
          type="submit" 
          class="btn btn-primary" 
          :disabled="loading"
        >
          {{ loading ? 'Creating account...' : 'Register' }}
        </button>
        
        <div class="login-link">
          Already have an account? <router-link to="/login">Login</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const username = ref('');
const password = ref('');
const birthday = ref('');
const error = ref('');
const loading = ref(false);

const handleRegister = async () => {
  if (!username.value || !password.value || !birthday.value) {
    error.value = 'Please fill in all fields';
    return;
  }
  
  loading.value = true;
  error.value = '';
  
  try {
    await axios.post('/users', {
      username: username.value,
      password: password.value,
      birthday: birthday.value
    });
    
    // Show success message
    alert('Account created successfully! You can now login.');
    router.push('/login');
  } catch (err) {
    if (err.response?.status === 409) {
      error.value = 'Username already exists. Please choose another one.';
    } else {
      error.value = err.response?.data?.detail || 'Failed to create account. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 0 auto;
}

h1 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  text-align: center;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

button {
  width: 100%;
  margin-top: 0.5rem;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.login-link a {
  color: #4285f4;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>