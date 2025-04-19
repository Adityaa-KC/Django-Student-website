/**
 * JavaScript for handling the application form functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // File upload preview functionality
    const photoInput = document.getElementById('photoInput');
    const signatureInput = document.getElementById('signatureInput');
    const photoPreview = document.getElementById('photoPreview');
    const signaturePreview = document.getElementById('signaturePreview');
    
    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function(event) {
            previewImage(event, photoPreview);
            validateFileSize(photoInput, 'photo');
        });
    }
    
    if (signatureInput && signaturePreview) {
        signatureInput.addEventListener('change', function(event) {
            previewImage(event, signaturePreview);
            validateFileSize(signatureInput, 'signature');
        });
    }
    
    // Form validation
    const applicationForm = document.getElementById('applicationForm');
    if (applicationForm) {
        applicationForm.addEventListener('submit', function(event) {
            if (!validateForm()) {
                event.preventDefault();
            }
        });
    }
});

/**
 * Function to preview uploaded image
 * @param {Event} event - The change event
 * @param {HTMLElement} previewElement - The image element to display the preview
 */
function previewImage(event, previewElement) {
    const file = event.target.files[0];
    if (file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            alert('Invalid file type. Please upload a JPG, JPEG, or PNG file.');
            event.target.value = '';
            previewElement.classList.add('d-none');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.classList.remove('d-none');
        };
        reader.readAsDataURL(file);
    } else {
        previewElement.classList.add('d-none');
    }
}

/**
 * Function to validate file size
 * @param {HTMLElement} inputElement - The file input element
 * @param {string} fileType - The type of file (photo or signature)
 * @returns {boolean} - True if valid, false otherwise
 */
function validateFileSize(inputElement, fileType) {
    const file = inputElement.files[0];
    if (file) {
        // Check file size (max 10MB)
        const maxSize = 10 * 1024 * 1024; // 10MB in bytes
        if (file.size > maxSize) {
            alert(`The ${fileType} file size exceeds the maximum limit of 10MB. Please upload a smaller file.`);
            inputElement.value = '';
            return false;
        }
    }
    return true;
}

/**
 * Function to validate the entire application form
 * @returns {boolean} - True if valid, false otherwise
 */
function validateForm() {
    let isValid = true;
    
    // Validate all required fields
    const requiredFields = document.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Validate mobile number (10 digits)
    const mobileField = document.querySelector('input[name="mobile_number"]');
    if (mobileField && mobileField.value) {
        const mobileRegex = /^\d{10}$/;
        if (!mobileRegex.test(mobileField.value)) {
            isValid = false;
            mobileField.classList.add('is-invalid');
            if (!mobileField.nextElementSibling || !mobileField.nextElementSibling.classList.contains('invalid-feedback')) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'invalid-feedback';
                errorMsg.textContent = 'Mobile number must be 10 digits';
                mobileField.parentNode.insertBefore(errorMsg, mobileField.nextSibling);
            }
        }
    }
    
    // Validate Aadhar number (12 digits)
    const aadharField = document.querySelector('input[name="aadhar_number"]');
    if (aadharField && aadharField.value) {
        const aadharRegex = /^\d{12}$/;
        if (!aadharRegex.test(aadharField.value)) {
            isValid = false;
            aadharField.classList.add('is-invalid');
            if (!aadharField.nextElementSibling || !aadharField.nextElementSibling.classList.contains('invalid-feedback')) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'invalid-feedback';
                errorMsg.textContent = 'Aadhar number must be 12 digits';
                aadharField.parentNode.insertBefore(errorMsg, aadharField.nextSibling);
            }
        }
    }
    
    // Validate email format
    const emailField = document.querySelector('input[name="email"]');
    if (emailField && emailField.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value)) {
            isValid = false;
            emailField.classList.add('is-invalid');
            if (!emailField.nextElementSibling || !emailField.nextElementSibling.classList.contains('invalid-feedback')) {
                const errorMsg = document.createElement('div');
                errorMsg.className = 'invalid-feedback';
                errorMsg.textContent = 'Please enter a valid email address';
                emailField.parentNode.insertBefore(errorMsg, emailField.nextSibling);
            }
        }
    }
    
    // Validate file uploads
    const photoInput = document.getElementById('photoInput');
    const signatureInput = document.getElementById('signatureInput');
    
    if (photoInput && !validateFileSize(photoInput, 'photo')) {
        isValid = false;
    }
    
    if (signatureInput && !validateFileSize(signatureInput, 'signature')) {
        isValid = false;
    }
    
    if (!isValid) {
        alert('Please correct the errors in the form before proceeding.');
    }
    
    return isValid;
}
