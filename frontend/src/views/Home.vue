<template>
  <div class="space-y-8">
    <!-- Hero Section -->
    <div class="text-center py-12">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">
        Welcome to Harmoniq
      </h1>
      <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
        Discover and organize your music with our powerful streaming platform. 
        Connect with Tidal and create your perfect playlists.
      </p>
      <div class="flex justify-center space-x-4">
        <router-link 
          to="/tracks" 
          class="btn-primary text-lg px-8 py-3"
        >
          Browse Tracks
        </router-link>
        <router-link 
          v-if="isAuthenticated"
          to="/playlists" 
          class="btn-secondary text-lg px-8 py-3"
        >
          My Playlists
        </router-link>
        <router-link 
          v-else
          to="/register" 
          class="btn-secondary text-lg px-8 py-3"
        >
          Get Started
        </router-link>
      </div>
    </div>

    <!-- Features Section -->
    <div class="grid md:grid-cols-3 gap-8">
      <div class="card text-center">
        <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Music Discovery</h3>
        <p class="text-gray-600">
          Explore millions of tracks from Tidal's extensive music library
        </p>
      </div>

      <div class="card text-center">
        <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Playlist Management</h3>
        <p class="text-gray-600">
          Create, organize, and share your favorite playlists
        </p>
      </div>

      <div class="card text-center">
        <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">Secure & Private</h3>
        <p class="text-gray-600">
          Your music preferences and playlists are kept private and secure
        </p>
      </div>
    </div>

    <!-- Stats Section -->
    <div v-if="isAuthenticated" class="card">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Your Music Stats</h2>
      <div class="grid md:grid-cols-3 gap-6">
        <div class="text-center">
          <div class="text-3xl font-bold text-primary-600">{{ stats.playlists || 0 }}</div>
          <div class="text-gray-600">Playlists</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-primary-600">{{ stats.tracks || 0 }}</div>
          <div class="text-gray-600">Tracks</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-primary-600">{{ stats.favorites || 0 }}</div>
          <div class="text-gray-600">Favorites</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { playlistsAPI, tracksAPI } from '../services/api'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    const stats = ref({ playlists: 0, tracks: 0, favorites: 0 })
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    const loadStats = async () => {
      if (isAuthenticated.value) {
        try {
          const [playlistsRes, tracksRes] = await Promise.all([
            playlistsAPI.getMyPlaylists(),
            tracksAPI.getAll({ limit: 1 })
          ])
          
          stats.value = {
            playlists: playlistsRes.data.length,
            tracks: tracksRes.data.length,
            favorites: 0 // TODO: Implement favorites API
          }
        } catch (error) {
          console.error('Error loading stats:', error)
        }
      }
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      isAuthenticated,
      stats
    }
  }
}
</script> 