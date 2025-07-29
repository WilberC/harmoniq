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

function initializeDockIcons() {
    // Add click effects to dock icons
    document.querySelectorAll('.dock-icon, [class*="w-12 h-12"]').forEach(icon => {
        icon.addEventListener('click', function() {
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}

function initializeDesktop() {
    // Initialize date/time updates
    updateDateTime();
    setInterval(updateDateTime, 1000);

    // Initialize dock icons
    initializeDockIcons();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeDesktop);
