// Main JavaScript file for V Mart Inventory Management

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    const deleteLinks = document.querySelectorAll('a[href*="/delete/"]');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form[novalidate]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                }
            }
            form.classList.add('was-validated');
        });
    });

    // Real-time search functionality
    const searchInput = document.getElementById('search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                // Auto-submit search form after 500ms of no typing
                if (searchInput.value.length >= 3 || searchInput.value.length === 0) {
                    searchInput.closest('form').submit();
                }
            }, 500);
        });
    }

    // Stock level progress bars animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(function() {
            bar.style.width = width;
            bar.style.transition = 'width 1s ease-in-out';
        }, 100);
    });

    // Table sorting functionality
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    sortableHeaders.forEach(function(header) {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const sortField = this.dataset.sort;
            const currentUrl = new URL(window.location);
            const currentSort = currentUrl.searchParams.get('sort');
            const currentOrder = currentUrl.searchParams.get('order');
            
            // Toggle order if same field, otherwise default to asc
            if (currentSort === sortField) {
                currentUrl.searchParams.set('order', currentOrder === 'asc' ? 'desc' : 'asc');
            } else {
                currentUrl.searchParams.set('sort', sortField);
                currentUrl.searchParams.set('order', 'asc');
            }
            
            window.location.href = currentUrl.toString();
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N for new product
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            const addButton = document.querySelector('a[href*="/add"]');
            if (addButton) {
                window.location.href = addButton.href;
            }
        }
        
        // Escape key to go back
        if (e.key === 'Escape') {
            const backButton = document.querySelector('a[href="/"]');
            if (backButton && window.location.pathname !== '/') {
                window.location.href = backButton.href;
            }
        }
    });

    // Loading states for buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            if (this.closest('form').checkValidity()) {
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                this.disabled = true;
            }
        });
    });

    // Auto-focus first form field
    const firstFormField = document.querySelector('form input:not([type="hidden"]), form select, form textarea');
    if (firstFormField && !firstFormField.value) {
        firstFormField.focus();
    }

    // Stock status color coding
    const stockBadges = document.querySelectorAll('.badge[data-stock]');
    stockBadges.forEach(function(badge) {
        const stock = parseInt(badge.dataset.stock);
        const minLevel = parseInt(badge.dataset.minLevel) || 10;
        
        badge.classList.remove('bg-success', 'bg-warning', 'bg-danger');
        
        if (stock === 0) {
            badge.classList.add('bg-danger');
        } else if (stock <= minLevel) {
            badge.classList.add('bg-warning', 'text-dark');
        } else {
            badge.classList.add('bg-success');
        }
    });

    // Price formatting
    const priceInputs = document.querySelectorAll('input[name="price"]');
    priceInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });

    // Mobile menu improvements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: true
                    });
                }
            });
        });
    }

    // Print functionality
    const printButton = document.getElementById('printButton');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }

    // Export functionality placeholder
    const exportButton = document.getElementById('exportButton');
    if (exportButton) {
        exportButton.addEventListener('click', function() {
            // This would typically connect to a backend export endpoint
            alert('Export functionality would be implemented here');
        });
    }
});

// Utility functions
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

function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showNotification('An unexpected error occurred. Please refresh the page.', 'danger');
});