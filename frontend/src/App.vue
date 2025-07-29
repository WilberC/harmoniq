<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <h1 class="text-xl font-bold text-primary-600">Harmoniq</h1>
            </router-link>
          </div>
          
          <div class="flex items-center space-x-4">
            <router-link 
              to="/" 
              class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Home
            </router-link>
            <router-link 
              to="/tracks" 
              class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Tracks
            </router-link>
            <router-link 
              to="/playlists" 
              class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Playlists
            </router-link>
            
            <div v-if="!isAuthenticated" class="flex items-center space-x-2">
              <router-link 
                to="/login" 
                class="btn-secondary text-sm"
              >
                Login
              </router-link>
              <router-link 
                to="/register" 
                class="btn-primary text-sm"
              >
                Register
              </router-link>
            </div>
            
            <div v-else class="flex items-center space-x-2">
              <span class="text-sm text-gray-700">{{ user?.username }}</span>
              <button 
                @click="logout" 
                class="btn-secondary text-sm"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
    
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const user = computed(() => authStore.user)
    
    const logout = () => {
      authStore.logout()
    }
    
    return {
      isAuthenticated,
      user,
      logout
    }
  }
}
</script> 