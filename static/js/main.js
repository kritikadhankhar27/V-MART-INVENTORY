// V Mart Inventory Management System - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeSearch();
    initializeAlerts();
    initializeTooltips();
    initializeFormValidation();
    initializeImagePreview();
    initializeStockAlerts();
    
    console.log('V Mart Inventory System initialized successfully');
});

// Search and Filter Functionality
function initializeSearch() {
    const searchForm = document.querySelector('form[method="GET"]');
    const searchInput = document.getElementById('search');
    
    if (searchInput) {
        // Add real-time search with debouncing
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3 || this.value.length === 0) {
                    performSearch();
                }
            }, 500);
        });
    }
    
    // Auto-submit form on filter change
    const filterSelects = document.querySelectorAll('#category, #stock, #sort');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            if (searchForm) {
                searchForm.submit();
            }
        });
    });
}

function performSearch() {
    const form = document.querySelector('form[method="GET"]');
    if (form) {
        form.submit();
    }
}

// Alert System
function initializeAlerts() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
    
    // Add animation to alerts
    alerts.forEach(alert => {
        alert.classList.add('fade-in');
    });
}

// Bootstrap Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (form.classList.contains('was-validated')) {
                    this.classList.toggle('is-valid', this.checkValidity());
                    this.classList.toggle('is-invalid', !this.checkValidity());
                }
            });
        });
    });
}

// Image Preview Functionality
function initializeImagePreview() {
    const imageUrlInputs = document.querySelectorAll('input[name="image_url"]');
    
    imageUrlInputs.forEach(input => {
        input.addEventListener('input', function() {
            const previewContainer = document.getElementById('image-preview');
            const previewImg = document.getElementById('preview-img');
            
            if (previewContainer && previewImg) {
                const url = this.value.trim();
                
                if (url) {
                    previewImg.src = url;
                    previewContainer.style.display = 'block';
                    
                    previewImg.onload = function() {
                        previewContainer.classList.add('fade-in');
                    };
                    
                    previewImg.onerror = function() {
                        previewContainer.style.display = 'none';
                        showToast('Invalid image URL', 'warning');
                    };
                } else {
                    previewContainer.style.display = 'none';
                }
            }
        });
    });
}

// Stock Level Monitoring
function initializeStockAlerts() {
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    const minStockInputs = document.querySelectorAll('input[name="min_stock_level"]');
    
    function checkStockLevel() {
        const quantityInput = document.getElementById('quantity');
        const minStockInput = document.getElementById('min_stock_level');
        
        if (quantityInput && minStockInput) {
            const quantity = parseInt(quantityInput.value) || 0;
            const minStock = parseInt(minStockInput.value) || 0;
            
            // Remove existing classes
            quantityInput.classList.remove('border-success', 'border-warning', 'border-danger');
            
            if (quantity === 0) {
                quantityInput.classList.add('border-danger');
                showStockAlert('Out of stock!', 'danger');
            } else if (quantity <= minStock) {
                quantityInput.classList.add('border-warning');
                showStockAlert('Low stock warning!', 'warning');
            } else {
                quantityInput.classList.add('border-success');
            }
        }
    }
    
    quantityInputs.forEach(input => {
        input.addEventListener('input', checkStockLevel);
    });
    
    minStockInputs.forEach(input => {
        input.addEventListener('input', checkStockLevel);
    });
}

function showStockAlert(message, type) {
    // Remove existing stock alerts
    const existingAlerts = document.querySelectorAll('.stock-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show stock-alert mt-2`;
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const quantityInput = document.getElementById('quantity');
    if (quantityInput) {
        quantityInput.parentNode.appendChild(alertDiv);
        
        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            if (alertDiv) {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }
        }, 3000);
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    return container;
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(dateString));
}

// Card Animation
function animateCard(card) {
    card.style.transform = 'scale(0.95)';
    card.style.transition = 'transform 0.1s ease';
    
    setTimeout(() => {
        card.style.transform = 'scale(1)';
    }, 100);
}

// Add click animation to product cards
document.addEventListener('click', function(e) {
    const card = e.target.closest('.product-card');
    if (card) {
        animateCard(card);
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('search');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        const searchInput = document.getElementById('search');
        if (searchInput && searchInput === document.activeElement) {
            searchInput.value = '';
            searchInput.blur();
            performSearch();
        }
    }
});

// Print functionality
function printInventory() {
    window.print();
}

// Export functionality (if needed)
function exportInventory(format = 'csv') {
    showToast('Export functionality would be implemented here', 'info');
}

// Loading states
function showLoading(element) {
    if (element) {
        element.classList.add('loading');
        const spinner = document.createElement('div');
        spinner.className = 'spinner-border spinner-border-sm me-2';
        element.insertBefore(spinner, element.firstChild);
    }
}

function hideLoading(element) {
    if (element) {
        element.classList.remove('loading');
        const spinner = element.querySelector('.spinner-border');
        if (spinner) {
            spinner.remove();
        }
    }
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showToast('An unexpected error occurred. Please refresh the page.', 'danger');
});

// Service worker registration (for offline functionality)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Service worker would be registered here for offline functionality
        console.log('Service worker support detected');
    });
}

// Performance monitoring
function measurePerformance() {
    if (window.performance && window.performance.timing) {
        const timing = window.performance.timing;
        const loadTime = timing.loadEventEnd - timing.navigationStart;
        console.log(`Page load time: ${loadTime}ms`);
    }
}

// Call performance measurement after load
window.addEventListener('load', measurePerformance);

// Auto-save functionality for forms (draft saving)
function initializeAutoSave() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);
                
                // Save to localStorage as draft
                localStorage.setItem(`vmart_draft_${form.id || 'form'}`, JSON.stringify(data));
            });
        });
    });
}

// Initialize auto-save if forms are present
if (document.querySelector('form')) {
    initializeAutoSave();
}

