// Preload logo image
document.addEventListener('DOMContentLoaded', function() {
    // Preload the logo image
    const logoImage = new Image();
    logoImage.src = '/static/images/logo.png';
    
    // Add logo click handler to redirect to home
    const logoContainers = document.querySelectorAll('.logo-container');
    logoContainers.forEach(container => {
        container.addEventListener('click', function() {
            window.location.href = '/';
        });
        container.style.cursor = 'pointer';
    });
    
    // Sidebar Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const sidebarClose = document.getElementById('sidebar-close');
    
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('sidebar-collapsed');
        sidebar.classList.toggle('sidebar-expanded');
        mainContent.classList.toggle('main-content-expanded');
    });
    
    if (sidebarClose) {
        sidebarClose.addEventListener('click', function() {
            sidebar.classList.add('sidebar-collapsed');
            sidebar.classList.remove('sidebar-expanded');
            mainContent.classList.add('main-content-expanded');
        });
    }
    
    // Sidebar Menu Navigation
    const sidebarMenuItems = document.querySelectorAll('.sidebar-menu-item[data-tab]');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    sidebarMenuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            sidebarMenuItems.forEach(menuItem => {
                menuItem.classList.remove('active');
            });
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Hide all tab panes
            tabPanes.forEach(pane => {
                pane.classList.remove('show', 'active');
            });
            
            // Show selected tab pane
            const tabId = this.getAttribute('data-tab');
            const tabPane = document.getElementById(tabId);
            if (tabPane) {
                tabPane.classList.add('show', 'active');
                document.querySelector('.header-title').textContent = tabId === 'dashboard' ? 'Dashboard' : tabPane.querySelector('.card-header h5').textContent;
            }
        });
    });

    // Navigation to About page
    const aboutLink = document.getElementById('aboutLink');
    if (aboutLink) {
        aboutLink.addEventListener('click', function() {
            window.location.href = '/about';
        });
    }
    
    // Feature buttons navigation
    const startDetectionBtn = document.getElementById('startDetectionBtn');
    if (startDetectionBtn) {
        startDetectionBtn.addEventListener('click', function() {
            document.querySelector('.sidebar-menu-item[data-tab="weeddetection"]').click();
        });
    }
    
    const weedDetectionFeatureBtn = document.getElementById('weedDetectionFeatureBtn');
    if (weedDetectionFeatureBtn) {
        weedDetectionFeatureBtn.addEventListener('click', function() {
            document.querySelector('.sidebar-menu-item[data-tab="weeddetection"]').click();
        });
    }
    
    const growthStageFeatureBtn = document.getElementById('growthStageFeatureBtn');
    if (growthStageFeatureBtn) {
        growthStageFeatureBtn.addEventListener('click', function() {
            document.querySelector('.sidebar-menu-item[data-tab="growthstage"]').click();
        });
    }
    
    const documentAnalysisFeatureBtn = document.getElementById('documentAnalysisFeatureBtn');
    if (documentAnalysisFeatureBtn) {
        documentAnalysisFeatureBtn.addEventListener('click', function() {
            document.querySelector('.sidebar-menu-item[data-tab="docanalysis"]').click();
        });
    }

    // Set up drag and drop functionality for all upload containers
    function setupDragAndDrop(container, input) {
        if (!container || !input) return;
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            container.addEventListener(eventName, preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            container.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            container.addEventListener(eventName, unhighlight, false);
        });

        container.addEventListener('drop', function(e) {
            let dt = e.dataTransfer;
            input.files = dt.files;
            const event = new Event('change');
            input.dispatchEvent(event);
        }, false);

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        function highlight() {
            container.classList.add('highlight');
        }

        function unhighlight() {
            container.classList.remove('highlight');
        }
    }

    // Weed Detection
    const weedUploadContainer = document.getElementById('weedUploadContainer');
    const weedImageInput = document.getElementById('weedImageInput');
    const weedResults = document.getElementById('weedResults');
    const annotatedImage = document.getElementById('annotatedImage');
    const weedInfo = document.getElementById('weedInfo');

    if (weedUploadContainer && weedImageInput) {
        setupDragAndDrop(weedUploadContainer, weedImageInput);
        
        weedUploadContainer.addEventListener('click', function() {
            weedImageInput.click();
        });

        weedImageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const formData = new FormData();
                formData.append('file', this.files[0]);
                
                // Show loading state
                weedUploadContainer.style.display = 'none';
                weedResults.style.display = 'block';
                weedInfo.innerHTML = '<div class="spinner"></div><p class="text-center mt-3">Processing your image with YOLOv12...</p>';
                
                fetch('/upload_image', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Display the results
                        annotatedImage.src = `/static/uploads/${data.filename}`;
                        document.getElementById('modelVersion').textContent = data.results.model || 'YOLOv12';
                        document.getElementById('inferenceTime').textContent = data.results.inference_time || '0.0s';
                        document.getElementById('confidenceThreshold').textContent = data.results.confidence_threshold || '0.0';
                        document.getElementById('detectionsCount').textContent = data.results.detections.length || '0';
                        
                        // Update new YOLOv12 specific fields
                        if (document.getElementById('neuralArch')) {
                            document.getElementById('neuralArch').textContent = data.results.architecture || 'TransformerS-Vision';
                        }
                        if (document.getElementById('resolution')) {
                            const dimensions = data.results.image_dimensions || [1280, 1280];
                            document.getElementById('resolution').textContent = `${dimensions[0]}×${dimensions[1]}`;
                        }
                        if (document.getElementById('realtimeFps')) {
                            document.getElementById('realtimeFps').textContent = '120';
                        }
                        
                        // Display environmental analysis if available
                        let environmentalHtml = '';
                        if (data.results.environmental_analysis) {
                            environmentalHtml = `
                                <div class="card mt-4">
                                    <div class="card-header">
                                        <h5 class="mb-0">Environmental Analysis</h5>
                                    </div>
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-md-4 col-6 mb-3">
                                                <div class="mb-1"><strong>Soil Moisture:</strong></div>
                                                <div>${data.results.environmental_analysis.soil_moisture}</div>
                                            </div>
                                            <div class="col-md-4 col-6 mb-3">
                                                <div class="mb-1"><strong>Light Conditions:</strong></div>
                                                <div>${data.results.environmental_analysis.light_conditions}</div>
                                            </div>
                                            <div class="col-md-4 col-6 mb-3">
                                                <div class="mb-1"><strong>Soil Compaction:</strong></div>
                                                <div>${data.results.environmental_analysis.estimated_soil_compaction}</div>
                                            </div>
                                            <div class="col-md-6 col-6 mb-3">
                                                <div class="mb-1"><strong>Competition Factor:</strong></div>
                                                <div>${data.results.environmental_analysis.competition_factor}</div>
                                            </div>
                                            <div class="col-md-6 col-6">
                                                <div class="mb-1"><strong>Recommended Treatment:</strong></div>
                                                <div>${data.results.environmental_analysis.recommended_treatment_timing}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                        }
                        
                        let weedHtml = '';
                        data.results.detections.forEach((weed, index) => {
                            weedHtml += `
                                <div class="weed-item">
                                    <h5>${weed.weed_type} <span class="badge bg-primary">${(weed.confidence * 100).toFixed(1)}%</span></h5>
                                    <div class="row mb-3">
                                        <div class="col-md-4 col-6">
                                            <div class="mb-1"><strong>Growth Stage:</strong></div>
                                            <div>${weed.growth_stage || 'Unknown'}</div>
                                        </div>
                                        <div class="col-md-4 col-6">
                                            <div class="mb-1"><strong>Health Status:</strong></div>
                                            <div>${weed.health_status || 'Unknown'}</div>
                                        </div>
                                        <div class="col-md-4 col-6">
                                            <div class="mb-1"><strong>Size:</strong></div>
                                            <div>${weed.size_cm ? weed.size_cm + ' cm' : 'Unknown'}</div>
                                        </div>
                                    </div>
                                    <div class="accordion mb-3">
                                        <div class="accordion-item">
                                            <h2 class="accordion-header">
                                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#info${index}">
                                                    Scientific Information
                                                </button>
                                            </h2>
                                            <div id="info${index}" class="accordion-collapse collapse">
                                                <div class="accordion-body">
                                                    <p><strong>Scientific Name:</strong> ${weed.scientific_name || 'Not available'}</p>
                                                    <p><strong>Growth Pattern:</strong> ${weed.growth_pattern || 'Not available'}</p>
                                                    <p><strong>Habitat:</strong> ${weed.habitat || 'Not available'}</p>
                                                    <p><strong>Estimated Age:</strong> ${weed.estimated_age_days ? weed.estimated_age_days + ' days' : 'Unknown'}</p>
                                                    <p><strong>Density Score:</strong> ${weed.density_score || 'Unknown'}</p>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="accordion-item">
                                            <h2 class="accordion-header">
                                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#remedy${index}">
                                                    Control Methods
                                                </button>
                                            </h2>
                                            <div id="remedy${index}" class="accordion-collapse collapse">
                                                <div class="accordion-body">
                                                    <p><strong>Organic Control:</strong> ${weed.remedy?.organic || 'Not available'}</p>
                                                    <p><strong>Chemical Control:</strong> ${weed.remedy?.chemical || 'Not available'}</p>
                                                    <p><strong>Prevention:</strong> ${weed.remedy?.prevention || 'Not available'}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                        });
                        weedInfo.innerHTML = weedHtml + environmentalHtml || '<p class="text-center">No weeds detected in this image.</p>';
                    } else {
                        weedInfo.innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
                        weedUploadContainer.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    weedInfo.innerHTML = '<div class="alert alert-danger">An error occurred while processing your request.</div>';
                    weedUploadContainer.style.display = 'block';
                });
            }
        });
    }

    // Growth Stage Detection
    const growthUploadContainer = document.getElementById('growthUploadContainer');
    const growthImageInput = document.getElementById('growthImageInput');
    const growthResults = document.getElementById('growthResults');
    const growthImage = document.getElementById('growthImage');
    const growthInfo = document.getElementById('growthInfo');

    if (growthUploadContainer && growthImageInput) {
        setupDragAndDrop(growthUploadContainer, growthImageInput);
        
        growthUploadContainer.addEventListener('click', function() {
            growthImageInput.click();
        });

        growthImageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const formData = new FormData();
                formData.append('file', this.files[0]);
                
                // Show loading state
                growthUploadContainer.style.display = 'none';
                growthResults.style.display = 'block';
                growthInfo.innerHTML = '<div class="spinner"></div><p class="text-center mt-3">Analyzing growth stage...</p>';
                
                fetch('/detect_growth_stage', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Display the results
                        growthImage.src = `/static/uploads/${data.filename}`;
                        
                        let infoHtml = `
                            <div class="text-center mb-4">
                                <h2>${data.growth_stage}</h2>
                                <p class="badge bg-primary">Confidence: ${(data.confidence * 100).toFixed(1)}%</p>
                            </div>
                            <div class="mb-3">
                                <h5>Features Detected:</h5>
                                <ul class="list-group">
                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                        Green Percentage
                                        <span class="badge bg-primary rounded-pill">${data.features.green_percentage}%</span>
                                    </li>
                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                        Plant Count
                                        <span class="badge bg-primary rounded-pill">${data.features.plant_count}</span>
                                    </li>
                                </ul>
                            </div>
                        `;
                        
                        if (data.characteristics) {
                            infoHtml += `
                                <div class="mb-3">
                                    <h5>Stage Characteristics:</h5>
                                    <p>${data.characteristics}</p>
                                </div>
                            `;
                        }
                        
                        if (data.recommendations && data.recommendations.length > 0) {
                            infoHtml += `
                                <div class="mb-3">
                                    <h5>Management Recommendations:</h5>
                                    <ul class="list-group">
                            `;
                            
                            data.recommendations.forEach(rec => {
                                infoHtml += `
                                    <li class="list-group-item">
                                        <i class="bi bi-check-circle-fill text-success me-2"></i> ${rec}
                                    </li>
                                `;
                            });
                            
                            infoHtml += `
                                    </ul>
                                </div>
                            `;
                        }
                        
                        growthInfo.innerHTML = infoHtml;
                    } else {
                        growthInfo.innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
                        growthUploadContainer.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    growthInfo.innerHTML = '<div class="alert alert-danger">An error occurred while processing your request.</div>';
                    growthUploadContainer.style.display = 'block';
                });
            }
        });
    }

    // Document Analysis
    const docUploadContainer = document.getElementById('docUploadContainer');
    const documentInput = document.getElementById('documentInput');
    const docResults = document.getElementById('docResults');
    const docSummary = document.getElementById('docSummary');
    const reportLink = document.getElementById('reportLink');

    if (docUploadContainer && documentInput) {
        setupDragAndDrop(docUploadContainer, documentInput);
        
        docUploadContainer.addEventListener('click', function() {
            documentInput.click();
        });

        documentInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const formData = new FormData();
                formData.append('document', this.files[0]);
                
                // Show loading state
                docUploadContainer.style.display = 'none';
                docResults.style.display = 'block';
                docSummary.innerHTML = '<div class="spinner"></div><p class="text-center mt-3">Analyzing document...</p>';
                
                fetch('/upload_document', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Display the results
                        reportLink.href = data.report_path;
                        
                        let summaryHtml = `
                            <p>${data.analysis.summary}</p>
                            <div class="row mt-4">
                                <div class="col-md-6">
                                    <h5>Weed Mentions</h5>
                                    <ul class="list-group">
                        `;
                        
                        for (const [weed, count] of Object.entries(data.analysis.weed_mentions)) {
                            summaryHtml += `
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    ${weed}
                                    <span class="badge bg-primary rounded-pill">${count}</span>
                                </li>
                            `;
                        }
                        
                        summaryHtml += `
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h5>Growth Stages</h5>
                                    <ul class="list-group">
                        `;
                        
                        for (const [stage, count] of Object.entries(data.analysis.growth_stages)) {
                            summaryHtml += `
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    ${stage}
                                    <span class="badge bg-primary rounded-pill">${count}</span>
                                </li>
                            `;
                        }
                        
                        summaryHtml += `
                                    </ul>
                                </div>
                            </div>
                        `;
                        
                        docSummary.innerHTML = summaryHtml;
                    } else {
                        docSummary.innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
                        docUploadContainer.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    docSummary.innerHTML = '<div class="alert alert-danger">An error occurred while processing your request.</div>';
                    docUploadContainer.style.display = 'block';
                });
            }
        });
    }
    
    // Add a "Try Again" button functionality to all result sections
    const addTryAgainButtons = () => {
        // Weed Detection
        const weedResults = document.getElementById('weedResults');
        if (weedResults) {
            const weedTryAgainBtn = document.createElement('button');
            weedTryAgainBtn.className = 'btn btn-outline-primary mt-3';
            weedTryAgainBtn.innerHTML = '<i class="bi bi-arrow-repeat me-2"></i>Try Another Image';
            weedTryAgainBtn.onclick = function() {
                document.getElementById('weedUploadContainer').style.display = 'block';
                weedResults.style.display = 'none';
                document.getElementById('weedImageInput').value = '';
            };
            weedResults.appendChild(weedTryAgainBtn);
        }
        
        // Growth Stage
        const growthResults = document.getElementById('growthResults');
        if (growthResults) {
            const growthTryAgainBtn = document.createElement('button');
            growthTryAgainBtn.className = 'btn btn-outline-primary mt-3';
            growthTryAgainBtn.innerHTML = '<i class="bi bi-arrow-repeat me-2"></i>Try Another Image';
            growthTryAgainBtn.onclick = function() {
                document.getElementById('growthUploadContainer').style.display = 'block';
                growthResults.style.display = 'none';
                document.getElementById('growthImageInput').value = '';
            };
            growthResults.appendChild(growthTryAgainBtn);
        }
        
        // Document Analysis
        const docResults = document.getElementById('docResults');
        if (docResults) {
            const docTryAgainBtn = document.createElement('button');
            docTryAgainBtn.className = 'btn btn-outline-primary mt-3';
            docTryAgainBtn.innerHTML = '<i class="bi bi-arrow-repeat me-2"></i>Try Another Document';
            docTryAgainBtn.onclick = function() {
                document.getElementById('docUploadContainer').style.display = 'block';
                docResults.style.display = 'none';
                document.getElementById('documentInput').value = '';
            };
            docResults.appendChild(docTryAgainBtn);
        }
    };
    
    // Add try again buttons
    addTryAgainButtons();
}); 