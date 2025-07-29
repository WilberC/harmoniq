import axios from 'axios'

export const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
}

export const tracksAPI = {
  getAll: (params) => api.get('/tracks', { params }),
  getById: (id) => api.get(`/tracks/${id}`),
  search: (query) => api.get(`/tracks/search/${query}`),
  create: (trackData) => api.post('/tracks', trackData),
}

export const playlistsAPI = {
  getAll: (params) => api.get('/playlists', { params }),
  getMyPlaylists: () => api.get('/playlists/my'),
  getById: (id) => api.get(`/playlists/${id}`),
  create: (playlistData) => api.post('/playlists', playlistData),
  update: (id, playlistData) => api.put(`/playlists/${id}`, playlistData),
  delete: (id) => api.delete(`/playlists/${id}`),
  addTrack: (playlistId, trackId) => api.post(`/playlists/${playlistId}/tracks/${trackId}`),
}

export const usersAPI = {
  getMe: () => api.get('/users/me'),
  getById: (id) => api.get(`/users/${id}`),
} 