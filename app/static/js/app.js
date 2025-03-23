document.addEventListener('DOMContentLoaded', function() {
    // Initialize the upload forms
    const uploadImageForm = document.getElementById('uploadImageForm');
    const growthStageForm = document.getElementById('growthStageForm');
    const documentUploadForm = document.getElementById('documentUploadForm');
    
    // Initialize image preview
    if (uploadImageForm) {
        const imageFile = document.getElementById('imageFile');
        const previewImage = document.getElementById('previewImage');
        const uploadPreview = document.getElementById('uploadPreview');
        const changeImage = document.getElementById('changeImage');
        
        imageFile.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    uploadPreview.classList.remove('d-none');
                    imageFile.classList.add('d-none');
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
        
        changeImage.addEventListener('click', function() {
            uploadPreview.classList.add('d-none');
            imageFile.classList.remove('d-none');
            imageFile.value = '';
        });
        
        uploadImageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!imageFile.files || !imageFile.files[0]) {
                showAlert('Please select an image file', 'warning');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', imageFile.files[0]);
            
            showLoading('detectionsList');
            document.getElementById('resultsCard').classList.remove('d-none');
            
            // Send the image for weed detection
            fetch('/upload_image', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    displayDetectionResults(data);
                } else {
                    showAlert(data.error || 'Unknown error occurred', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error processing the image: ' + error.message, 'danger');
            })
            .finally(() => {
                hideLoading('detectionsList');
            });
        });
    }
    
    // Growth stage detection form handling
    if (growthStageForm) {
        const growthStageFile = document.getElementById('growthStageFile');
        const previewGrowthImage = document.getElementById('previewGrowthImage');
        const growthPreview = document.getElementById('growthPreview');
        const changeGrowthImage = document.getElementById('changeGrowthImage');
        
        growthStageFile.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewGrowthImage.src = e.target.result;
                    growthPreview.classList.remove('d-none');
                    growthStageFile.classList.add('d-none');
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
        
        changeGrowthImage.addEventListener('click', function() {
            growthPreview.classList.add('d-none');
            growthStageFile.classList.remove('d-none');
            growthStageFile.value = '';
        });
        
        growthStageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!growthStageFile.files || !growthStageFile.files[0]) {
                showAlert('Please select an image file', 'warning');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', growthStageFile.files[0]);
            
            document.getElementById('growthResultsCard').classList.remove('d-none');
            showLoading('stageDetails');
            
            // Send the image for growth stage detection
            fetch('/detect_growth_stage', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    displayGrowthStageResults(data);
                } else {
                    showAlert(data.error || 'Unknown error occurred', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error processing the image: ' + error.message, 'danger');
            })
            .finally(() => {
                hideLoading('stageDetails');
            });
        });
    }
    
    // Document upload form handling
    if (documentUploadForm) {
        documentUploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const documentFile = document.getElementById('documentFile');
            
            if (!documentFile.files || !documentFile.files[0]) {
                showAlert('Please select a document file', 'warning');
                return;
            }
            
            const formData = new FormData();
            formData.append('document', documentFile.files[0]);
            
            document.getElementById('documentResultsCard').classList.remove('d-none');
            showLoading('documentAnalysis');
            
            // Send the document for analysis
            fetch('/upload_document', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    displayDocumentAnalysis(data);
                } else {
                    showAlert(data.error || 'Unknown error occurred', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error processing the document: ' + error.message, 'danger');
            })
            .finally(() => {
                hideLoading('documentAnalysis');
            });
        });
    }
    
    // Initialize tooltips
    initTooltips();
});

// Function to display weed detection results
function displayDetectionResults(data) {
    // Update the result image
    const resultImage = document.getElementById('resultImage');
    resultImage.src = `/static/uploads/${data.annotated_image}`;
    
    // Display the detection results
    const detectionsList = document.getElementById('detectionsList');
    detectionsList.innerHTML = '';
    
    if (data.detections && data.detections.length > 0) {
        data.detections.forEach(detection => {
            const weedItem = document.createElement('div');
            weedItem.className = 'weed-item';
            
            const confidencePercent = Math.round(detection.confidence * 100);
            
            weedItem.innerHTML = `
                <h5 class="text-success">${detection.weed_type}</h5>
                <div class="d-flex align-items-center mb-2">
                    <span class="me-2">Confidence:</span>
                    <div class="confidence-bar flex-grow-1">
                        <div class="confidence-value" style="width: ${confidencePercent}%"></div>
                    </div>
                    <span class="ms-2">${confidencePercent}%</span>
                </div>
                <div class="remedy-container">
                    <div class="remedy-tabs">
                        <ul class="nav nav-tabs" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#organic-${detection.id}" type="button" role="tab">Organic</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#chemical-${detection.id}" type="button" role="tab">Chemical</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" data-bs-toggle="tab" data-bs-target="#prevention-${detection.id}" type="button" role="tab">Prevention</button>
                            </li>
                        </ul>
                    </div>
                    <div class="tab-content remedy-content">
                        <div class="tab-pane fade show active" id="organic-${detection.id}" role="tabpanel">
                            <p>${detection.remedy.organic}</p>
                        </div>
                        <div class="tab-pane fade" id="chemical-${detection.id}" role="tabpanel">
                            <p>${detection.remedy.chemical}</p>
                        </div>
                        <div class="tab-pane fade" id="prevention-${detection.id}" role="tabpanel">
                            <p>${detection.remedy.prevention}</p>
                        </div>
                    </div>
                </div>
            `;
            
            detectionsList.appendChild(weedItem);
        });
        
        // Initialize the tab functionality for remedies
        initTooltips();
        
    } else {
        detectionsList.innerHTML = `
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>No weeds detected in the image
            </div>
        `;
    }
}

// Function to display growth stage results
function displayGrowthStageResults(data) {
    // Update the growth stage image
    const growthResultImage = document.getElementById('growthResultImage');
    if (data.detections && data.detections.annotated_image) {
        growthResultImage.src = `/static/uploads/${data.detections.annotated_image}`;
    } else {
        // If no annotated image, use the original image
        growthResultImage.src = `/static/uploads/${data.filename}`;
    }
    
    // Update the growth stage information
    const stageTitle = document.getElementById('stageTitle');
    const stageConfidence = document.getElementById('stageConfidence');
    const confidenceValue = document.getElementById('confidenceValue');
    const stageDetails = document.getElementById('stageDetails');
    
    stageTitle.innerText = data.growth_stage || 'Unknown Stage';
    
    const confidencePercent = Math.round((data.confidence || 0) * 100);
    stageConfidence.style.width = `${confidencePercent}%`;
    confidenceValue.innerText = `${confidencePercent}%`;
    
    // Create details HTML
    let detailsHtml = `<p><strong>Growth Stage:</strong> ${data.growth_stage || 'Unknown'}</p>`;
    
    if (data.features) {
        detailsHtml += `<p><strong>Green Coverage:</strong> ${Math.round(data.features.green_percentage)}%</p>`;
        detailsHtml += `<p><strong>Plant Count:</strong> ${data.features.plant_count || 0}</p>`;
    }
    
    // Add recommendations based on growth stage
    detailsHtml += `<h5 class="mt-3">Recommendations</h5>`;
    
    if (data.growth_stage === 'Seedling') {
        detailsHtml += `
            <ul>
                <li>Early intervention is most effective at this stage</li>
                <li>Manual removal is recommended while roots are small</li>
                <li>Apply pre-emergent herbicides for large areas</li>
                <li>Monitor soil moisture and avoid overwatering</li>
            </ul>
        `;
    } else if (data.growth_stage === 'Vegetative') {
        detailsHtml += `
            <ul>
                <li>Implement cultural control methods like mulching</li>
                <li>Post-emergent herbicides are effective at this stage</li>
                <li>Consider hoeing or tilling for mechanical control</li>
                <li>Competitive planting can help suppress weed growth</li>
            </ul>
        `;
    } else if (data.growth_stage === 'Flowering') {
        detailsHtml += `
            <ul>
                <li>Prevent seed production by removing flowering weeds</li>
                <li>Spot treatments with herbicides may be needed</li>
                <li>Mowing can prevent seed dispersal</li>
                <li>Avoid disturbing soil which may spread seeds</li>
            </ul>
        `;
    } else if (data.growth_stage === 'Mature') {
        detailsHtml += `
            <ul>
                <li>Focus on preventing seed dispersal</li>
                <li>Remove and properly dispose of mature plants</li>
                <li>Plan for more intensive control next season</li>
                <li>Consider soil treatment to address seed bank</li>
            </ul>
        `;
    } else {
        detailsHtml += `
            <ul>
                <li>Implement integrated weed management practices</li>
                <li>Combine mechanical, cultural, and chemical controls as needed</li>
                <li>Monitor regularly for new weed growth</li>
                <li>Maintain healthy desired plants to compete with weeds</li>
            </ul>
        `;
    }
    
    stageDetails.innerHTML = detailsHtml;
}

// Function to display document analysis results
function displayDocumentAnalysis(data) {
    const documentAnalysis = document.getElementById('documentAnalysis');
    const reportBtnContainer = document.getElementById('reportBtnContainer');
    const viewReportBtn = document.getElementById('viewReportBtn');
    
    if (data.analysis) {
        let html = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle me-2"></i>Document successfully analyzed
            </div>
            
            <div class="doc-analysis-item">
                <h5 class="text-success"><i class="fas fa-file-alt me-2"></i>Summary</h5>
                <p>${data.analysis.summary || 'No summary available.'}</p>
            </div>
        `;
        
        // Display weed mentions
        if (data.analysis.weed_mentions && Object.keys(data.analysis.weed_mentions).length > 0) {
            html += `
                <div class="doc-analysis-item">
                    <h5 class="text-success"><i class="fas fa-leaf me-2"></i>Weed Species Mentioned</h5>
                    <ul class="list-group list-group-flush">
            `;
            
            for (const [weed, count] of Object.entries(data.analysis.weed_mentions)) {
                html += `<li class="list-group-item d-flex justify-content-between align-items-center">
                    ${weed}
                    <span class="badge bg-success rounded-pill">${count}</span>
                </li>`;
            }
            
            html += `
                    </ul>
                </div>
            `;
        }
        
        // Display growth stages
        if (data.analysis.growth_stages && Object.keys(data.analysis.growth_stages).length > 0) {
            html += `
                <div class="doc-analysis-item">
                    <h5 class="text-success"><i class="fas fa-seedling me-2"></i>Growth Stages Mentioned</h5>
                    <ul class="list-group list-group-flush">
            `;
            
            for (const [stage, count] of Object.entries(data.analysis.growth_stages)) {
                html += `<li class="list-group-item d-flex justify-content-between align-items-center">
                    ${stage}
                    <span class="badge bg-success rounded-pill">${count}</span>
                </li>`;
            }
            
            html += `
                    </ul>
                </div>
            `;
        }
        
        documentAnalysis.innerHTML = html;
        
        // Update report button if report path is available
        if (data.report_path) {
            viewReportBtn.href = data.report_path;
            reportBtnContainer.classList.remove('d-none');
        }
    } else {
        documentAnalysis.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>${data.message || 'Error processing document'}
            </div>
        `;
    }
}

// Utility function to show an alert
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.classList.remove('show');
        setTimeout(() => alertDiv.remove(), 150);
    }, 5000);
}

// Utility function to show loading spinner
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const originalContent = element.innerHTML;
        element.setAttribute('data-original-content', originalContent);
        
        element.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
            </div>
        `;
    }
}

// Utility function to hide loading spinner
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const originalContent = element.getAttribute('data-original-content');
        if (originalContent) {
            element.innerHTML = originalContent;
            element.removeAttribute('data-original-content');
        }
    }
}

// Initialize Bootstrap tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
} 