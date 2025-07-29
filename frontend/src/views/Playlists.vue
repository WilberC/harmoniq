<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-900">My Playlists</h1>
      <button
        @click="showCreateModal = true"
        class="btn-primary"
      >
        Create Playlist
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card">
      <div class="text-center text-red-600">{{ error }}</div>
    </div>

    <!-- Playlists Grid -->
    <div v-else-if="playlists.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div
        v-for="playlist in playlists"
        :key="playlist.id"
        class="card hover:shadow-md transition-shadow duration-200 cursor-pointer"
        @click="viewPlaylist(playlist)"
      >
        <div class="aspect-square bg-gradient-to-br from-primary-100 to-primary-200 rounded-lg mb-4 flex items-center justify-center">
          <svg class="w-16 h-16 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
          </svg>
        </div>
        
        <div class="space-y-2">
          <h3 class="font-semibold text-gray-900 truncate">{{ playlist.name }}</h3>
          <p v-if="playlist.description" class="text-sm text-gray-600 truncate">{{ playlist.description }}</p>
          <div class="flex items-center justify-between">
            <span class="text-xs text-gray-500">
              {{ playlist.is_public ? 'Public' : 'Private' }}
            </span>
            <div class="flex space-x-2">
              <button
                @click.stop="editPlaylist(playlist)"
                class="text-sm text-gray-600 hover:text-gray-700"
              >
                Edit
              </button>
              <button
                @click.stop="deletePlaylist(playlist)"
                class="text-sm text-red-600 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="card text-center py-12">
      <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">No playlists yet</h3>
      <p class="text-gray-600 mb-4">Create your first playlist to get started.</p>
      <button
        @click="showCreateModal = true"
        class="btn-primary"
      >
        Create Playlist
      </button>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold text-gray-900 mb-4">
          {{ showEditModal ? 'Edit Playlist' : 'Create Playlist' }}
        </h2>
        
        <form @submit.prevent="handleSubmit">
          <div class="space-y-4">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">
                Playlist Name
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="input-field mt-1"
                placeholder="Enter playlist name"
              />
            </div>
            
            <div>
              <label for="description" class="block text-sm font-medium text-gray-700">
                Description (optional)
              </label>
              <textarea
                id="description"
                v-model="form.description"
                rows="3"
                class="input-field mt-1"
                placeholder="Enter playlist description"
              ></textarea>
            </div>
            
            <div class="flex items-center">
              <input
                id="is_public"
                v-model="form.is_public"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="is_public" class="ml-2 block text-sm text-gray-900">
                Make playlist public
              </label>
            </div>
          </div>
          
          <div class="flex justify-end space-x-3 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="submitting"
              class="btn-primary"
            >
              {{ submitting ? 'Saving...' : (showEditModal ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { playlistsAPI } from '../services/api'

export default {
  name: 'Playlists',
  setup() {
    const router = useRouter()
    const playlists = ref([])
    const loading = ref(false)
    const error = ref('')
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const submitting = ref(false)
    const editingPlaylist = ref(null)
    
    const form = reactive({
      name: '',
      description: '',
      is_public: false
    })
    
    const loadPlaylists = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await playlistsAPI.getMyPlaylists()
        playlists.value = response.data
      } catch (err) {
        error.value = 'Failed to load playlists'
        console.error('Error loading playlists:', err)
      } finally {
        loading.value = false
      }
    }
    
    const handleSubmit = async () => {
      submitting.value = true
      
      try {
        if (showEditModal.value) {
          await playlistsAPI.update(editingPlaylist.value.id, form)
        } else {
          await playlistsAPI.create(form)
        }
        
        closeModal()
        loadPlaylists()
      } catch (err) {
        error.value = 'Failed to save playlist'
        console.error('Error saving playlist:', err)
      } finally {
        submitting.value = false
      }
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      editingPlaylist.value = null
      form.name = ''
      form.description = ''
      form.is_public = false
    }
    
    const editPlaylist = (playlist) => {
      editingPlaylist.value = playlist
      form.name = playlist.name
      form.description = playlist.description || ''
      form.is_public = playlist.is_public
      showEditModal.value = true
    }
    
    const deletePlaylist = async (playlist) => {
      if (confirm(`Are you sure you want to delete "${playlist.name}"?`)) {
        try {
          await playlistsAPI.delete(playlist.id)
          loadPlaylists()
        } catch (err) {
          error.value = 'Failed to delete playlist'
          console.error('Error deleting playlist:', err)
        }
      }
    }
    
    const viewPlaylist = (playlist) => {
      router.push(`/playlists/${playlist.id}`)
    }
    
    onMounted(() => {
      loadPlaylists()
    })
    
    return {
      playlists,
      loading,
      error,
      showCreateModal,
      showEditModal,
      submitting,
      form,
      handleSubmit,
      closeModal,
      editPlaylist,
      deletePlaylist,
      viewPlaylist
    }
  }
}
</script> 