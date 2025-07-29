<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card">
      <div class="text-center text-red-600">{{ error }}</div>
    </div>

    <!-- Playlist Content -->
    <div v-else-if="playlist" class="space-y-6">
      <!-- Header -->
      <div class="flex items-start justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">{{ playlist.name }}</h1>
          <p v-if="playlist.description" class="text-gray-600 mt-2">{{ playlist.description }}</p>
          <div class="flex items-center space-x-4 mt-4 text-sm text-gray-500">
            <span>{{ playlist.is_public ? 'Public' : 'Private' }}</span>
            <span>{{ tracks.length }} tracks</span>
          </div>
        </div>
        
        <div class="flex space-x-2">
          <button
            @click="showAddTrackModal = true"
            class="btn-primary"
          >
            Add Track
          </button>
          <router-link
            to="/playlists"
            class="btn-secondary"
          >
            Back to Playlists
          </router-link>
        </div>
      </div>

      <!-- Tracks List -->
      <div v-if="tracks.length > 0" class="card">
        <div class="space-y-2">
          <div
            v-for="(track, index) in tracks"
            :key="track.id"
            class="flex items-center space-x-4 p-4 hover:bg-gray-50 rounded-lg transition-colors duration-200"
          >
            <div class="flex-shrink-0 w-12 h-12 bg-gray-200 rounded-lg overflow-hidden">
              <img
                v-if="track.cover_url"
                :src="track.cover_url"
                :alt="track.title"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center bg-gray-300">
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
                </svg>
              </div>
            </div>
            
            <div class="flex-1 min-w-0">
              <h3 class="font-medium text-gray-900 truncate">{{ track.title }}</h3>
              <p class="text-sm text-gray-600 truncate">{{ track.artist }}</p>
              <p class="text-xs text-gray-500 truncate">{{ track.album }}</p>
            </div>
            
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-500">{{ formatDuration(track.duration) }}</span>
              <button
                v-if="track.preview_url"
                @click="playPreview(track)"
                class="text-gray-400 hover:text-gray-600"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </button>
              <button
                @click="removeTrack(track)"
                class="text-red-400 hover:text-red-600"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="card text-center py-12">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No tracks in this playlist</h3>
        <p class="text-gray-600 mb-4">Add some tracks to get started.</p>
        <button
          @click="showAddTrackModal = true"
          class="btn-primary"
        >
          Add Track
        </button>
      </div>
    </div>

    <!-- Add Track Modal -->
    <div v-if="showAddTrackModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Add Track to Playlist</h2>
        
        <div class="mb-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search tracks..."
            class="input-field"
            @input="searchTracks"
          />
        </div>
        
        <div v-if="searchLoading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        
        <div v-else-if="searchResults.length > 0" class="space-y-2 max-h-96 overflow-y-auto">
          <div
            v-for="track in searchResults"
            :key="track.id"
            class="flex items-center space-x-4 p-3 hover:bg-gray-50 rounded-lg cursor-pointer"
            @click="addTrack(track)"
          >
            <div class="flex-shrink-0 w-10 h-10 bg-gray-200 rounded overflow-hidden">
              <img
                v-if="track.cover_url"
                :src="track.cover_url"
                :alt="track.title"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center bg-gray-300">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
                </svg>
              </div>
            </div>
            
            <div class="flex-1 min-w-0">
              <h3 class="font-medium text-gray-900 truncate">{{ track.title }}</h3>
              <p class="text-sm text-gray-600 truncate">{{ track.artist }}</p>
            </div>
            
            <div class="text-sm text-gray-500">
              {{ formatDuration(track.duration) }}
            </div>
          </div>
        </div>
        
        <div v-else-if="searchQuery" class="text-center py-8 text-gray-500">
          No tracks found matching "{{ searchQuery }}"
        </div>
        
        <div class="flex justify-end mt-6">
          <button
            @click="showAddTrackModal = false"
            class="btn-secondary"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { playlistsAPI, tracksAPI } from '../services/api'

export default {
  name: 'PlaylistDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const playlist = ref(null)
    const tracks = ref([])
    const loading = ref(false)
    const error = ref('')
    const showAddTrackModal = ref(false)
    const searchQuery = ref('')
    const searchResults = ref([])
    const searchLoading = ref(false)
    
    const loadPlaylist = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await playlistsAPI.getById(route.params.id)
        playlist.value = response.data
        // TODO: Load tracks for this playlist
        tracks.value = []
      } catch (err) {
        error.value = 'Failed to load playlist'
        console.error('Error loading playlist:', err)
      } finally {
        loading.value = false
      }
    }
    
    const searchTracks = async () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = []
        return
      }
      
      searchLoading.value = true
      
      try {
        const response = await tracksAPI.search(searchQuery.value)
        searchResults.value = response.data
      } catch (err) {
        console.error('Error searching tracks:', err)
        searchResults.value = []
      } finally {
        searchLoading.value = false
      }
    }
    
    const addTrack = async (track) => {
      try {
        await playlistsAPI.addTrack(playlist.value.id, track.id)
        showAddTrackModal.value = false
        searchQuery.value = ''
        searchResults.value = []
        // TODO: Reload playlist tracks
      } catch (err) {
        console.error('Error adding track:', err)
      }
    }
    
    const removeTrack = async (track) => {
      if (confirm(`Remove "${track.title}" from this playlist?`)) {
        try {
          // TODO: Implement remove track API
          console.log('Remove track:', track)
        } catch (err) {
          console.error('Error removing track:', err)
        }
      }
    }
    
    const formatDuration = (seconds) => {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
    }
    
    const playPreview = (track) => {
      if (track.preview_url) {
        const audio = new Audio(track.preview_url)
        audio.play()
      }
    }
    
    onMounted(() => {
      loadPlaylist()
    })
    
    return {
      playlist,
      tracks,
      loading,
      error,
      showAddTrackModal,
      searchQuery,
      searchResults,
      searchLoading,
      searchTracks,
      addTrack,
      removeTrack,
      formatDuration,
      playPreview
    }
  }
}
</script> 