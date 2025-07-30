// Desktop JavaScript Functionality

function updateDateTime() {
    const now = new Date();
    const options = {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    };
    const dateTimeString = now.toLocaleDateString('en-US', options);
    const dateTimeElement = document.getElementById('dateTime');
    if (dateTimeElement) {
        dateTimeElement.textContent = dateTimeString;
    }
}

function closeModal(modalType) {
    const modal = document.getElementById(`${modalType}-modal`);

    if (modal) {
        // Hide modal
        modal.classList.remove('active');

        // Hide overlay if no other modals are active
        const activeModals = document.querySelectorAll('.modal.active');
        if (activeModals.length === 0) {
            const overlay = document.getElementById('modal-overlay');
            if (overlay) {
                overlay.classList.remove('active');
            }

            // Disable pointer events on container
            document.getElementById('modal-container').style.pointerEvents = 'none';
        }
    }
}

function openModal(modalType, clickedElement = null) {
    const modal = document.getElementById(`${modalType}-modal`);

    if (modal) {
        // Check if this modal is already active
        if (modal.classList.contains('active')) {
            // If already active, close it (toggle behavior)
            closeModal(modalType);
            return;
        }

        // Show modal
        modal.classList.add('active');

        // Show overlay if not already visible
        const overlay = document.getElementById('modal-overlay');
        if (overlay && !overlay.classList.contains('active')) {
            overlay.classList.add('active');
        }

        // Enable pointer events on container
        document.getElementById('modal-container').style.pointerEvents = 'auto';

        // Add bounce effect to dock icon
        if (clickedElement) {
            clickedElement.classList.add('bounce-effect');
            setTimeout(() => {
                clickedElement.classList.remove('bounce-effect');
            }, 400);
        }
    }
}

function initializeDockIcons() {
    document.querySelectorAll('.dock-icon[data-modal]').forEach(icon => {
        icon.addEventListener('click', function() {
            const modalType = this.getAttribute('data-modal');
            openModal(modalType, this);
        });
    });
}

function initializeModalCloseHandlers() {
    // Add event listeners for close buttons and cancel buttons
    document.querySelectorAll('[data-modal]').forEach(element => {
        element.addEventListener('click', function() {
            const modalType = this.getAttribute('data-modal');

            // Check if this is a close/cancel button (not a dock icon)
            if (this.classList.contains('modal-close') ||
                (this.classList.contains('btn') && this.classList.contains('btn-secondary'))) {
                closeModal(modalType);
            }
        });
    });

    // Add event listener for overlay click to close modal
    const overlay = document.getElementById('modal-overlay');
    if (overlay) {
        overlay.addEventListener('click', function() {
            // Find the currently active modal and close it
            const activeModal = document.querySelector('.modal.active');
            if (activeModal) {
                const modalId = activeModal.id;
                const modalType = modalId.replace('-modal', '');
                closeModal(modalType);
            }
        });
    }

    // Add event listener for escape key to close modal
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            const activeModal = document.querySelector('.modal.active');
            if (activeModal) {
                const modalId = activeModal.id;
                const modalType = modalId.replace('-modal', '');
                closeModal(modalType);
            }
        }
    });
}

function initializeDesktop() {
    // Initialize date/time updates
    updateDateTime();
    setInterval(updateDateTime, 1000);

    // Initialize dock icons
    initializeDockIcons();

    // Initialize modal close handlers
    initializeModalCloseHandlers();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeDesktop);
