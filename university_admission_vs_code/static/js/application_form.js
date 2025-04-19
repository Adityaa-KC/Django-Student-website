// Application form JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Image preview functionality
    function setupImagePreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);
        
        if (input && preview) {
            input.addEventListener('change', function() {
                const file = this.files[0];
                if (file) {
                    // Validate file type
                    const fileType = file.type;
                    if (!fileType.match('image/jpeg') && !fileType.match('image/png')) {
                        alert('Please select a JPEG or PNG image.');
                        this.value = '';
                        return;
                    }
                    
                    // Validate file size (max 10MB)
                    if (file.size > 10 * 1024 * 1024) {
                        alert('File size exceeds 10MB. Please select a smaller file.');
                        this.value = '';
                        return;
                    }
                    
                    // Preview the image
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        while (preview.firstChild) {
                            preview.removeChild(preview.firstChild);
                        }
                        
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.className = 'img-fluid';
                        preview.appendChild(img);
                        
                        // Additional validation for signature dimensions
                        if (inputId === 'signature') {
                            const tempImg = new Image();
                            tempImg.src = e.target.result;
                            tempImg.onload = function() {
                                if (this.width > 400 || this.height > 200) {
                                    const dimensionWarning = document.createElement('div');
                                    dimensionWarning.className = 'alert alert-warning mt-2';
                                    dimensionWarning.textContent = 'Signature exceeds recommended dimensions (400x200px). It will be resized.';
                                    preview.parentNode.insertBefore(dimensionWarning, preview.nextSibling);
                                    
                                    setTimeout(() => {
                                        dimensionWarning.remove();
                                    }, 5000);
                                }
                            };
                        }
                    };
                    reader.readAsDataURL(file);
                } else {
                    // Reset preview
                    while (preview.firstChild) {
                        preview.removeChild(preview.firstChild);
                    }
                    
                    const placeholderText = document.createElement('div');
                    placeholderText.className = 'text-center text-muted';
                    placeholderText.textContent = previewId === 'photoPreview' ? 'Photo Preview' : 
                                                 (previewId === 'signaturePreview' ? 'Signature Preview' : 'Aadhar Card Preview');
                    preview.appendChild(placeholderText);
                }
            });
        }
    }
    
    // Setup image previews
    setupImagePreview('photo', 'photoPreview');
    setupImagePreview('signature', 'signaturePreview');
    setupImagePreview('aadhar_card', 'aadharPreview');
    
    // Form validation
    const form = document.getElementById('applicationForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            let valid = true;
            
            // Validate Aadhar number
            const aadharInput = document.getElementById('aadhar_number');
            if (aadharInput && !/^\d{12}$/.test(aadharInput.value)) {
                alert('Aadhar number must be exactly 12 digits.');
                valid = false;
            }
            
            // Validate mobile number
            const mobileInput = document.getElementById('mobile_number');
            if (mobileInput && !/^\d{10}$/.test(mobileInput.value)) {
                alert('Mobile number must be exactly 10 digits.');
                valid = false;
            }
            
            if (!valid) {
                event.preventDefault();
            }
        });
    }
});