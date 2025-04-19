document.addEventListener('DOMContentLoaded', function() {
    // Image preview functionality
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Get the preview container
            const docType = this.closest('form').querySelector('input[name="doc_type"]').value;
            const previewContainer = document.getElementById(`${docType}-preview-container`);
            
            if (this.files && this.files[0]) {
                const file = this.files[0];
                
                // Validate file type
                const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
                if (!validTypes.includes(file.type)) {
                    alert('Please select a valid image file (JPG, JPEG, PNG)');
                    this.value = '';
                    return;
                }
                
                // Validate file size (max 10MB)
                const maxSize = 10 * 1024 * 1024; // 10MB in bytes
                if (file.size > maxSize) {
                    alert('File size exceeds 10MB limit');
                    this.value = '';
                    return;
                }
                
                // Create a FileReader
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // Clear the container
                    previewContainer.innerHTML = '';
                    
                    // Create image element
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.alt = docType;
                    
                    // Add preview controls
                    const controlsDiv = document.createElement('div');
                    controlsDiv.className = 'preview-controls';
                    
                    const resetBtn = document.createElement('a');
                    resetBtn.href = '#';
                    resetBtn.className = 'btn btn-sm btn-danger';
                    resetBtn.innerHTML = '<i class="fas fa-undo"></i>';
                    resetBtn.addEventListener('click', function(evt) {
                        evt.preventDefault();
                        input.value = '';
                        previewContainer.innerHTML = `
                            <div class="text-muted">
                                <i class="fas fa-${docType === 'photo' ? 'user' : docType === 'signature' ? 'signature' : 'id-card'} fa-3x mb-2"></i>
                                <p>No ${docType.replace('_', ' ')} uploaded</p>
                            </div>
                        `;
                    });
                    
                    controlsDiv.appendChild(resetBtn);
                    
                    // Special validation for signature dimensions
                    if (docType === 'signature') {
                        const imgObj = new Image();
                        imgObj.onload = function() {
                            const maxWidth = 400;
                            const maxHeight = 200;
                            
                            if (this.width > maxWidth || this.height > maxHeight) {
                                const warningDiv = document.createElement('div');
                                warningDiv.className = 'alert alert-warning mt-2 small';
                                warningDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-1"></i>Image dimensions (${this.width}×${this.height}) exceed the maximum allowed (400×200). The image will be resized when uploaded.`;
                                previewContainer.appendChild(warningDiv);
                            }
                        };
                        imgObj.src = e.target.result;
                    }
                    
                    previewContainer.appendChild(img);
                    previewContainer.appendChild(controlsDiv);
                };
                
                reader.readAsDataURL(file);
            }
        });
    });
});
