// static/generator/js/app.js
/**
 * Main JavaScript for Image Caption Generator
 * Implements all UI interactions described in Chapter 4
 */

class ImageCaptionApp {
    constructor() {
        this.initializeEventListeners();
        this.setupFileUpload();
    }

    initializeEventListeners() {
        // File upload handling
        const fileInput = document.getElementById('imageInput');
        const uploadArea = document.getElementById('fileUploadArea');
        
        if (fileInput && uploadArea) {
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
            
            // Drag and Drop
            uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
            uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
            uploadArea.addEventListener('drop', (e) => this.handleFileDrop(e));

            // Click placeholder to trigger file input
            const placeholder = document.querySelector('.upload-placeholder');
            placeholder.addEventListener('click', (e) => {
                if (e.target === placeholder || placeholder.contains(e.target)) {
                    fileInput.click();
                }
            });
        }

        // Close modal on outside click
        const modal = document.getElementById('correctionModal');
        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                this.closeModal();
            }
        });
    }

    setupFileUpload() {
        const fileInput = document.getElementById('imageInput');
        const generateBtn = document.getElementById('generateBtn');
        
        const updateState = () => {
            if (fileInput.files.length > 0) {
                generateBtn.disabled = false;
                this.showImagePreview(fileInput.files[0]);
            } else {
                generateBtn.disabled = true;
                this.resetUploadState();
            }
        };

        fileInput.addEventListener('change', updateState);
    }

    resetUploadState() {
        const preview = document.getElementById('uploadPreview');
        const placeholder = document.querySelector('.upload-placeholder');
        
        if (preview && placeholder) {
            preview.style.display = 'none';
            placeholder.style.display = 'block';
        }
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file && this.validateImageFile(file)) {
            // Nothing more needed, setupFileUpload handles preview logic
        } else {
            // Reset file input if validation fails
            event.target.value = null; 
            this.resetUploadState();
            document.getElementById('generateBtn').disabled = true;
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('dragover');
    }

    handleDragLeave(event) {
        event.currentTarget.classList.remove('dragover');
    }

    handleFileDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0 && this.validateImageFile(files[0])) {
            // Set the file to the input element and trigger change event
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(files[0]);
            const fileInput = document.getElementById('imageInput');
            fileInput.files = dataTransfer.files;
            fileInput.dispatchEvent(new Event('change'));
        }
    }

    validateImageFile(file) {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        const maxSize = 5 * 1024 * 1024; // 5MB
        
        if (!validTypes.includes(file.type)) {
            this.showNotification('Please select a valid image file (JPG, PNG, JPEG)', 'error');
            return false;
        }
        
        if (file.size > maxSize) {
            this.showNotification('File size must be less than 5MB', 'error');
            return false;
        }
        
        return true;
    }

    showImagePreview(file) {
        const reader = new FileReader();
        const preview = document.getElementById('uploadPreview');
        const previewImg = document.getElementById('imagePreview');
        const placeholder = document.querySelector('.upload-placeholder');
        
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            if (placeholder && preview) {
                placeholder.style.display = 'none';
                preview.style.display = 'flex';
            }
        };
        
        reader.readAsDataURL(file);
    }

    showNotification(message, type = 'info') {
        const container = document.getElementById('notification-container');
        if (!container) return;

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;
        
        // Add to container
        container.appendChild(notification);
        
        // Remove after a delay
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    getNotificationIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    closeModal() {
        document.getElementById('correctionModal').style.display = 'none';
    }
}

// Global variable to hold the single instance of the app
let appInstance = null;

// Global functions for template (will use appInstance)
function copyToClipboard(text) {
    if (!appInstance) appInstance = new ImageCaptionApp();
    navigator.clipboard.writeText(text).then(() => {
        appInstance.showNotification('Caption copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Could not copy text: ', err);
        appInstance.showNotification('Failed to copy caption.', 'error');
    });
}

function showCorrectionModal(imageId, currentCaption) {
    if (!appInstance) appInstance = new ImageCaptionApp();
    document.getElementById('correctionImageId').value = imageId;
    document.getElementById('userCaption').value = currentCaption;
    document.getElementById('correctionModal').style.display = 'block';
}

function closeModal() {
    if (!appInstance) appInstance = new ImageCaptionApp();
    appInstance.closeModal();
}

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

function submitFeedback(action, imageId) {
    if (!appInstance) appInstance = new ImageCaptionApp();

    const formData = new FormData();
    formData.append('action', action);
    formData.append('image_id', imageId);
    
    fetch('/api/caption-feedback/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            appInstance.showNotification(data.message, 'success');
        } else {
            appInstance.showNotification(data.message || 'Feedback submission failed.', 'error');
        }
    })
    .catch(error => {
        console.error('Error submitting feedback:', error);
        appInstance.showNotification('Error submitting feedback.', 'error');
    });
}

function submitCorrection() {
    if (!appInstance) appInstance = new ImageCaptionApp();

    const imageId = document.getElementById('correctionImageId').value;
    const userCaption = document.getElementById('userCaption').value;
    const datasetPurpose = document.getElementById('datasetPurpose').value;
    
    if (!userCaption.trim()) {
        appInstance.showNotification('Correction caption cannot be empty.', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('action', 'correct');
    formData.append('image_id', imageId);
    formData.append('user_caption', userCaption);
    formData.append('dataset_split', datasetPurpose);
    
    fetch('/api/caption-feedback/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            appInstance.showNotification(data.message, 'success');
            appInstance.closeModal();
        } else {
            appInstance.showNotification(data.message || 'Correction submission failed.', 'error');
        }
    })
    .catch(error => {
        console.error('Error submitting correction:', error);
        appInstance.showNotification('Error submitting correction.', 'error');
    });
}


// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the app instance globally
    appInstance = new ImageCaptionApp();
});