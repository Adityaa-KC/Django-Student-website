/**
 * JavaScript for handling the application preview functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize preview form
    const previewForm = document.getElementById('previewForm');
    const editButton = document.querySelector('button[name="edit"]');
    const submitButton = document.querySelector('button[name="confirm_submit"]');
    
    if (previewForm) {
        // Confirm submission
        if (submitButton) {
            submitButton.addEventListener('click', function(event) {
                if (!confirm('Are you sure you want to submit your application? This action cannot be undone.')) {
                    event.preventDefault();
                }
            });
        }
    }
});
