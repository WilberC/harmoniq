/**
 * Main JavaScript file for Harmoniq
 * Handles drag-and-drop functionality, AJAX requests, and UI interactions
 */

// Global variables
let sortableInstances = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeSortable();
    initializeEventListeners();
});

// Initialize Sortable.js for drag-and-drop functionality
function initializeSortable() {
    // Initialize playlist grid sortable
    const playlistGrid = document.querySelector('.playlists-grid');
    if (playlistGrid) {
        const playlistSortable = new Sortable(playlistGrid, {
            animation: 150,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            onEnd: function(evt) {
                handlePlaylistReorder(evt);
            }
        });
        sortableInstances.push(playlistSortable);
    }

    // Initialize track grid sortable
    const trackGrid = document.querySelector('.tracks-grid');
    if (trackGrid) {
        const trackSortable = new Sortable(trackGrid, {
            animation: 150,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            group: 'tracks', // Allow moving between playlists
            onEnd: function(evt) {
                handleTrackMove(evt);
            }
        });
        sortableInstances.push(trackSortable);
    }
}

// Handle playlist reordering
function handlePlaylistReorder(evt) {
    const playlistId = evt.item.dataset.playlistId;
    const newPosition = evt.newIndex + 1;
    
    // Call API to update playlist position
    fetch('/api/playlists/reorder/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            playlist_id: playlistId,
            new_position: newPosition
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Playlist reordered successfully');
        } else {
            console.error('Error reordering playlist:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Handle track movement between playlists
function handleTrackMove(evt) {
    const trackId = evt.item.dataset.trackId;
    const newPlaylistId = evt.to.dataset.playlistId;
    const newPosition = evt.newIndex + 1;
    
    // Call API to move track
    fetch('/api/tracks/move/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            track_id: trackId,
            new_playlist_id: newPlaylistId,
            new_position: newPosition
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Track moved successfully');
            showNotification('Track moved successfully', 'success');
        } else {
            console.error('Error moving track:', data.error);
            showNotification('Error moving track', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error moving track', 'error');
    });
}

// Initialize event listeners
function initializeEventListeners() {
    // Modal event listeners
    const modals = document.querySelectorAll('.modal-overlay');
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.add('hidden');
            }
        });
    });

    // Form submission listeners
    const forms = document.querySelectorAll('form[up-target]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add loading state
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>Loading...';
            }
        });
    });
}

// Get CSRF token from the page
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all duration-300 transform translate-x-full`;
    
    // Set background color based on type
    switch (type) {
        case 'success':
            notification.className += ' bg-green-500 text-white';
            break;
        case 'error':
            notification.className += ' bg-red-500 text-white';
            break;
        case 'warning':
            notification.className += ' bg-yellow-500 text-white';
            break;
        default:
            notification.className += ' bg-blue-500 text-white';
    }
    
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        const debouncedSearch = debounce(function(query) {
            performSearch(query);
        }, 300);
        
        searchInput.addEventListener('input', function(e) {
            debouncedSearch(e.target.value);
        });
    }
}

function performSearch(query) {
    if (query.length < 2) {
        // Clear search results
        return;
    }
    
    fetch(`/api/search/?q=${encodeURIComponent(query)}`, {
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        displaySearchResults(data);
    })
    .catch(error => {
        console.error('Search error:', error);
    });
}

function displaySearchResults(results) {
    // Implementation for displaying search results
    console.log('Search results:', results);
}

// Export functions for global use
window.Harmoniq = {
    showNotification,
    initializeSortable,
    getCSRFToken
};