<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">Music Tracks</h1>
      <div class="flex space-x-2">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search tracks..."
          class="input-field w-64"
          @input="handleSearch"
        />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card">
      <div class="text-center text-red-600">{{ error }}</div>
    </div>

    <!-- Tracks Grid -->
    <div v-else-if="tracks.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div
        v-for="track in tracks"
        :key="track.id"
        class="card hover:shadow-md transition-shadow duration-200 cursor-pointer"
        @click="selectTrack(track)"
      >
        <div class="aspect-square bg-gray-200 rounded-lg mb-4 overflow-hidden">
          <img
            v-if="track.cover_url"
            :src="track.cover_url"
            :alt="track.title"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center bg-gray-300">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
            </svg>
          </div>
        </div>
        
        <div class="space-y-2">
          <h3 class="font-semibold text-gray-900 truncate">{{ track.title }}</h3>
          <p class="text-sm text-gray-600 truncate">{{ track.artist }}</p>
          <p class="text-xs text-gray-500 truncate">{{ track.album }}</p>
          <p class="text-xs text-gray-400">{{ formatDuration(track.duration) }}</p>
        </div>
        
        <div class="mt-4 flex justify-between items-center">
          <button
            v-if="isAuthenticated"
            @click.stop="addToPlaylist(track)"
            class="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Add to Playlist
          </button>
          <button
            v-if="track.preview_url"
            @click.stop="playPreview(track)"
            class="text-sm text-gray-600 hover:text-gray-700"
          >
            Preview
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="card text-center py-12">
      <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">No tracks found</h3>
      <p class="text-gray-600">Try adjusting your search or browse all tracks.</p>
    </div>

    <!-- Load More -->
    <div v-if="hasMore && !loading" class="text-center">
      <button
        @click="loadMore"
        class="btn-secondary"
      >
        Load More
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { tracksAPI } from '../services/api'

export default {
  name: 'Tracks',
  setup() {
    const authStore = useAuthStore()
    const tracks = ref([])
    const loading = ref(false)
    const error = ref('')
    const searchQuery = ref('')
    const page = ref(1)
    const hasMore = ref(true)
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    const loadTracks = async (reset = false) => {
      if (reset) {
        page.value = 1
        tracks.value = []
      }
      
      loading.value = true
      error.value = ''
      
      try {
        const params = {
          skip: (page.value - 1) * 20,
          limit: 20
        }
        
        if (searchQuery.value) {
          params.search = searchQuery.value
        }
        
        const response = await tracksAPI.getAll(params)
        const newTracks = response.data
        
        if (reset) {
          tracks.value = newTracks
        } else {
          tracks.value.push(...newTracks)
        }
        
        hasMore.value = newTracks.length === 20
      } catch (err) {
        error.value = 'Failed to load tracks'
        console.error('Error loading tracks:', err)
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      loadTracks(true)
    }
    
    const loadMore = () => {
      page.value++
      loadTracks()
    }
    
    const formatDuration = (seconds) => {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
    }
    
    const selectTrack = (track) => {
      console.log('Selected track:', track)
      // TODO: Implement track selection/playback
    }
    
    const addToPlaylist = (track) => {
      console.log('Add to playlist:', track)
      // TODO: Implement add to playlist functionality
    }
    
    const playPreview = (track) => {
      if (track.preview_url) {
        const audio = new Audio(track.preview_url)
        audio.play()
      }
    }
    
    onMounted(() => {
      loadTracks()
    })
    
    return {
      tracks,
      loading,
      error,
      searchQuery,
      hasMore,
      isAuthenticated,
      handleSearch,
      loadMore,
      formatDuration,
      selectTrack,
      addToPlaylist,
      playPreview
    }
  }
}
</script> 