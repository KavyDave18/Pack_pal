/**
 * Notification System
 * A simple notification system for showing success, error, and info messages
 */

// Store notification elements
const notification = document.getElementById('notification');
const notificationContent = notification ? notification.querySelector('.notification-content') : null;
const notificationIcon = notification ? notification.querySelector('.notification-icon') : null;
const notificationMessage = notification ? notification.querySelector('.notification-message') : null;
const notificationClose = notification ? notification.querySelector('.notification-close') : null;

// Notification timeout
let notificationTimeout;

/**
 * Show a notification message
 * @param {string} type - Type of notification (success, error, info)
 * @param {string} message - Notification message
 * @param {number} duration - Duration in milliseconds (default: 5000)
 */
function showNotification(type, message, duration = 5000) {
    if (!notification || !notificationContent || !notificationIcon || !notificationMessage) {
        console.error('Notification elements not found');
        return;
    }
    
    // Clear any existing timeout
    if (notificationTimeout) {
        clearTimeout(notificationTimeout);
    }
    
    // Set notification type
    notification.className = 'notification';
    notification.classList.add(`notification-${type}`);
    
    // Set icon based on type
    let iconClass = 'fas ';
    switch (type) {
        case 'success':
            iconClass += 'fa-check-circle';
            break;
        case 'error':
            iconClass += 'fa-exclamation-circle';
            break;
        case 'info':
        default:
            iconClass += 'fa-info-circle';
            break;
    }
    notificationIcon.className = iconClass;
    
    // Set message
    notificationMessage.textContent = message;
    
    // Show notification
    notification.classList.add('show');
    
    // Auto-hide after duration
    notificationTimeout = setTimeout(() => {
        notification.classList.remove('show');
    }, duration);
}

// Close notification on click
if (notificationClose) {
    notificationClose.addEventListener('click', function() {
        notification.classList.remove('show');
        if (notificationTimeout) {
            clearTimeout(notificationTimeout);
        }
    });
}

// Make function available globally
window.showNotification = showNotification;