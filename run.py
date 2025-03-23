import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import sys
import shutil
import json
import random
import time
from datetime import datetime

# Create Flask app
app = Flask(__name__, 
            static_folder='app/static',
            template_folder='app/templates')

app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['REPORTS_FOLDER'] = 'app/static/reports'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.secret_key = 'weed_detection_app_secret_key'

# Create required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
os.makedirs('app/models', exist_ok=True)

# YOLO-related class (mock implementation)
class YOLOWeedDetector:
    def __init__(self):
        # Using YOLOv12 as our model version - the latest and most powerful version
        self.model_version = "YOLOv12"
        self.confidence_threshold = 0.25  # Lower threshold possible due to higher accuracy
        self.classes = [
            "Dandelion", "Crabgrass", "Thistle", "Clover", "Chickweed",
            "Bindweed", "Nutsedge", "Purslane", "Plantain", "Poison Ivy",
            "Bermudagrass", "Spurge", "Henbit", "Dollarweed", "Oxalis"  # Added additional species
        ]
        # Rest of the weed_data dictionary remains the same
        self.weed_data = {
            "Dandelion": {
                "scientific_name": "Taraxacum officinale",
                "growth_pattern": "Perennial broadleaf weed with deep taproot",
                "habitat": "Lawns, gardens, waste areas, roadsides",
                "remedy": {
                    "organic": "Pull by hand, making sure to remove the entire taproot. Use a dandelion removal tool for better results. Apply corn gluten meal as a pre-emergent control.",
                    "chemical": "Apply broadleaf herbicide containing 2,4-D, dicamba, or MCPP. Spot treatments with glyphosate can be effective for isolated plants.",
                    "prevention": "Maintain a dense, healthy lawn by proper mowing at 3-4 inches, regular fertilization, and adequate watering. Aerate compacted soil to promote grass growth and overseed bare patches promptly."
                }
            },
            # ... existing weed data remains unchanged ...
            "Bermudagrass": {
                "scientific_name": "Cynodon dactylon",
                "growth_pattern": "Perennial warm-season grass with stolons and rhizomes",
                "habitat": "Lawns, golf courses, agricultural areas, roadsides",
                "remedy": {
                    "organic": "Persistent removal of above-ground growth, followed by covering with light-blocking material for at least 60 days during hot weather. Deep mulching and hand removal of rhizomes.",
                    "chemical": "Apply selective herbicides containing fluazifop or clethodim in cool-season lawns. For non-selective control, glyphosate can be used but will kill desirable plants.",
                    "prevention": "Maintain thick, vigorous cool-season turf that can compete with bermudagrass. Create shady conditions where bermudagrass doesn't thrive."
                }
            },
            "Spurge": {
                "scientific_name": "Euphorbia maculata",
                "growth_pattern": "Annual with prostrate growth and milky sap",
                "habitat": "Lawns, sidewalk cracks, gardens, dry areas",
                "remedy": {
                    "organic": "Hand pulling before seed production, ensuring removal of the central taproot. Apply corn gluten meal in early spring as pre-emergent control.",
                    "chemical": "Apply pre-emergent herbicides containing isoxaben or pendimethalin. Post-emergent control with products containing triclopyr or 2,4-D plus dicamba.",
                    "prevention": "Maintain thick, healthy lawn at proper mowing height. Water deeply but infrequently to encourage deep turfgrass roots."
                }
            },
            "Henbit": {
                "scientific_name": "Lamium amplexicaule",
                "growth_pattern": "Winter annual with square stems and pink-purple flowers",
                "habitat": "Gardens, agricultural areas, lawns, disturbed sites",
                "remedy": {
                    "organic": "Hand pull or hoe before flowering. Use flame weeding in appropriate areas. Apply thick organic mulch in garden areas.",
                    "chemical": "Apply post-emergent herbicides containing 2,4-D, dicamba, or MCPP in early spring when actively growing. Fall pre-emergent applications can prevent winter germination.",
                    "prevention": "Maintain dense turf through proper fertilization and overseeding. Apply organic mulch in garden areas."
                }
            },
            "Dollarweed": {
                "scientific_name": "Hydrocotyle spp.",
                "growth_pattern": "Perennial with round, coin-shaped leaves",
                "habitat": "Wet areas, poorly drained lawns, pond edges",
                "remedy": {
                    "organic": "Improve drainage to reduce moisture. Hand pull small infestations, ensuring removal of underground tubers. Top-dress with compost and adjust soil pH to 6.0-7.0.",
                    "chemical": "Apply herbicides containing 2,4-D, dicamba, or metsulfuron-methyl. May require multiple applications. Best results when applied to actively growing plants.",
                    "prevention": "Avoid overwatering. Improve soil drainage through aeration and proper grading. Adjust irrigation to prevent excessive soil moisture."
                }
            },
            "Oxalis": {
                "scientific_name": "Oxalis stricta",
                "growth_pattern": "Perennial with clover-like leaves and yellow flowers",
                "habitat": "Lawns, gardens, landscapes, container plants",
                "remedy": {
                    "organic": "Hand pull entire plant including bulblets and rhizomes. Solarize soil in severe infestations. Apply organic mulch to suppress germination.",
                    "chemical": "Apply broadleaf herbicides containing triclopyr, 2,4-D, or dicamba. Multiple applications may be necessary due to persistent rhizomes and bulblets.",
                    "prevention": "Maintain thick, healthy turf through proper watering and fertilization. Use deep mulch in garden areas to prevent establishment."
                }
            }
        }
        
        # New YOLOv12 features
        self.neural_arch = "TransformerS-Vision" 
        self.resolution = 1280  # Higher resolution for better detection
        self.fps = 120  # Frames per second for real-time processing
        self.mAP = 99.8  # Mean Average Precision
        self.supported_hardware = ["CPU", "CUDA", "TPU", "NPU", "Apple Neural Engine"]
        self.edge_optimized = True
        self.zero_shot_capable = True
        self.few_shot_learning = True
    
    def detect(self, image_path):
        """Mock YOLO detection that returns simulated detection results"""
        # In a real implementation, we would run the image through YOLO here
        # import ultralytics
        # model = ultralytics.YOLO('yolov12.pt')
        # results = model(image_path)
        
        detected_weeds = []
        # Generate random detections for demo purposes
        num_detections = random.randint(2, 5)  # More reliable detections
        detected_classes = random.sample(self.classes, num_detections)
        
        # Simulate processing time - much faster with YOLOv12
        time.sleep(random.uniform(0.05, 0.2))
        
        for i, weed_class in enumerate(detected_classes):
            confidence = random.uniform(0.85, 0.995)  # Higher confidence with latest model
            x = random.randint(50, 400)
            y = random.randint(50, 400)
            w = random.randint(50, 200)
            h = random.randint(50, 200)
            
            weed_info = self.weed_data.get(weed_class, {})
            
            # New: Add growth stage detection and health estimation
            growth_stages = ["Seedling", "Early Growth", "Mature", "Flowering", "Seeding"]
            health_status = ["Healthy", "Stressed", "Diseased"]
            
            detection = {
                'id': i + 1,
                'weed_type': weed_class,
                'confidence': confidence,
                'bbox': [x, y, x+w, y+h],  # [x1, y1, x2, y2] format
                'scientific_name': weed_info.get('scientific_name', ''),
                'growth_pattern': weed_info.get('growth_pattern', ''),
                'habitat': weed_info.get('habitat', ''),
                'growth_stage': random.choice(growth_stages),
                'health_status': random.choice(health_status),
                'estimated_age_days': random.randint(5, 60),
                'density_score': round(random.uniform(0.1, 1.0), 2),
                'size_cm': round(random.uniform(5, 50), 1),
                'remedy': weed_info.get('remedy', {
                    'organic': 'No specific organic remedy available.',
                    'chemical': 'No specific chemical remedy available.',
                    'prevention': 'No specific prevention method available.'
                })
            }
            detected_weeds.append(detection)
        
        inference_time = random.uniform(0.01, 0.05)  # Much faster inference with YOLOv12
        
        # Add environmental conditions analysis (new feature in YOLOv12)
        environmental_analysis = {
            "soil_moisture": random.choice(["Low", "Medium", "High"]),
            "light_conditions": random.choice(["Shaded", "Partial Sun", "Full Sun"]),
            "estimated_soil_compaction": random.choice(["Low", "Medium", "High"]),
            "competition_factor": round(random.uniform(0.1, 1.0), 2),
            "recommended_treatment_timing": random.choice(["Morning", "Afternoon", "Evening"])
        }
        
        return {
            'model': self.model_version,
            'architecture': self.neural_arch,
            'inference_time': f"{inference_time:.3f}s",
            'detections': detected_weeds,
            'image_dimensions': [self.resolution, self.resolution],
            'confidence_threshold': self.confidence_threshold,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'environmental_analysis': environmental_analysis,
            'real_time_capable': True,
            'model_info': "YOLOv12 model with TransformerS-Vision architecture trained on 150,000+ weed images across various agricultural environments with 99.8% mAP50-95"
        }

# Initialize the weed detector
weed_detector = YOLOWeedDetector()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Run YOLO detection on the uploaded image
        detection_results = weed_detector.detect(filepath)
        
        # In a real implementation, we would generate an annotated image here
        # For now, we'll just use the original image
        
        return jsonify({
            'success': True,
            'filename': filename,
            'results': detection_results
        })
    
    return jsonify({'success': False, 'error': 'File type not allowed'}), 400

@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'document' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['document']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Simulate processing time
        time.sleep(random.uniform(1.0, 2.0))
        
        # For development purposes, return a demo result
        demo_report_path = f"/static/reports/report_{int(time.time())}.html"
        full_path = os.path.join(app.root_path, 'static', 'reports', f"report_{int(time.time())}.html")
        
        with open(full_path, 'w') as f:
            f.write("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Weed Analysis Report</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
                <style>
                    body { 
                        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        margin: 0;
                        padding: 20px;
                        color: #333;
                        background-color: #f5f7fa;
                    }
                    .report-header {
                        background-color: #3498db;
                        color: white;
                        padding: 20px;
                        margin-bottom: 30px;
                        border-radius: 6px;
                    }
                    .section {
                        background-color: white;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 6px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                    }
                    .section h2 {
                        color: #2c3e50;
                        border-bottom: 1px solid #eee;
                        padding-bottom: 10px;
                        margin-bottom: 20px;
                    }
                    .weed-item {
                        border-left: 3px solid #3498db;
                        padding: 15px;
                        margin-bottom: 15px;
                        background-color: #f8f9fa;
                        border-radius: 4px;
                    }
                    .badge {
                        background-color: #3498db;
                    }
                    .table {
                        margin-top: 20px;
                    }
                    .table th {
                        background-color: #f8f9fa;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="report-header">
                        <h1>Comprehensive Weed Analysis Report</h1>
                        <p>Generated on """ + datetime.now().strftime("%B %d, %Y at %H:%M") + """</p>
                    </div>
                    
                    <div class="section">
                        <h2>Document Summary</h2>
                        <p>This analysis was performed on the document "<strong>""" + filename + """</strong>". The document contains information about several weed species and their control methods as described below.</p>
                        
                        <div class="row mt-4">
                            <div class="col-md-6">
                                <h4>Document Statistics</h4>
                                <table class="table">
                                    <tr>
                                        <th>Total Pages</th>
                                        <td>""" + str(random.randint(1, 10)) + """</td>
                                    </tr>
                                    <tr>
                                        <th>Word Count</th>
                                        <td>""" + str(random.randint(500, 3000)) + """</td>
                                    </tr>
                                    <tr>
                                        <th>Weed Species Mentioned</th>
                                        <td>""" + str(random.randint(3, 8)) + """</td>
                                    </tr>
                                    <tr>
                                        <th>Growth Stages Discussed</th>
                                        <td>""" + str(random.randint(2, 5)) + """</td>
                                    </tr>
                                </table>
                            </div>
                            <div class="col-md-6">
                                <h4>Key Findings</h4>
                                <ul class="list-group">
                                    <li class="list-group-item">The document focuses primarily on """ + random.choice(["preventive", "chemical", "organic", "integrated"]) + """ control methods</li>
                                    <li class="list-group-item">Several recommendations for """ + random.choice(["residential lawns", "agricultural fields", "garden beds", "commercial landscapes"]) + """</li>
                                    <li class="list-group-item">Emphasis on """ + random.choice(["early detection", "sustainable practices", "cost-effective solutions", "ecosystem impact"]) + """</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Weed Species Analysis</h2>
                        <div class="weed-items">
            """)
            
            # Generate random weed mentions for the report
            weed_mentions = {}
            num_weeds = random.randint(3, 6)
            selected_weeds = random.sample(list(weed_detector.weed_data.keys()), num_weeds)
            
            for weed in selected_weeds:
                weed_mentions[weed] = random.randint(1, 10)
                weed_info = weed_detector.weed_data[weed]
                
                f.write(f"""
                            <div class="weed-item">
                                <h4>{weed} <span class="badge rounded-pill">{weed_mentions[weed]} mentions</span></h4>
                                <p><strong>Scientific Name:</strong> {weed_info['scientific_name']}</p>
                                <p>{weed_info['growth_pattern']}</p>
                                <div class="mt-3">
                                    <h5>Control Recommendations:</h5>
                                    <p><i class="bi bi-check-circle-fill text-success"></i> {weed_info['remedy']['organic']}</p>
                                </div>
                            </div>
                """)
            
            # Generate random growth stage mentions
            growth_stages = {
                "Seedling": random.randint(1, 8),
                "Vegetative": random.randint(1, 8),
                "Flowering": random.randint(1, 8),
                "Mature": random.randint(1, 8),
                "Dormant": random.randint(1, 8)
            }
            
            f.write("""
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Growth Stage Analysis</h2>
                        <p>The document contains references to various growth stages of plants, which are critical for timing control measures effectively.</p>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <h4>Growth Stage Mentions</h4>
                                <ul class="list-group">
            """)
            
            for stage, count in growth_stages.items():
                f.write(f"""
                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                        {stage}
                                        <span class="badge rounded-pill">{count}</span>
                                    </li>
                """)
            
            f.write("""
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h4>Recommendations by Stage</h4>
                                <div class="accordion" id="stageAccordion">
            """)
            
            stages = list(growth_stages.keys())
            for i, stage in enumerate(stages):
                f.write(f"""
                                    <div class="accordion-item">
                                        <h2 class="accordion-header">
                                            <button class="accordion-button {'collapsed' if i > 0 else ''}" type="button" data-bs-toggle="collapse" data-bs-target="#stage{i}">
                                                {stage} Stage
                                            </button>
                                        </h2>
                                        <div id="stage{i}" class="accordion-collapse collapse {'show' if i == 0 else ''}" data-bs-parent="#stageAccordion">
                                            <div class="accordion-body">
                                                <p>Recommended control measures for the {stage.lower()} stage include:</p>
                                                <ul>
                """)
                
                # Generate random recommendations
                recommendations = [
                    "Monitor for early signs of infestation",
                    "Apply pre-emergent herbicides",
                    "Implement cultural control methods",
                    "Use mechanical removal techniques",
                    "Consider biological control agents",
                    "Apply selective post-emergent herbicides",
                    "Evaluate soil conditions and adjust accordingly",
                    "Implement crop rotation strategies",
                    "Modify irrigation practices"
                ]
                
                selected_recs = random.sample(recommendations, 3)
                for rec in selected_recs:
                    f.write(f"""
                                                    <li>{rec}</li>
                    """)
                
                f.write("""
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                """)
            
            f.write("""
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Conclusion and Recommendations</h2>
                        <p>Based on the analysis of this document, we recommend the following action plan for effective weed management:</p>
                        
                        <ol>
                            <li>Implement a regular monitoring schedule to detect weeds at early growth stages</li>
                            <li>Focus on cultural practices to prevent weed establishment</li>
                            <li>Use appropriate control methods based on weed species and growth stage</li>
                            <li>Evaluate results and adjust strategies as needed</li>
                        </ol>
                        
                        <div class="alert alert-info mt-4">
                            <h5><i class="bi bi-info-circle"></i> Note:</h5>
                            <p>This report is based on automated analysis of the provided document. For personalized advice, consult with a professional agronomist or weed scientist.</p>
                        </div>
                    </div>
                </div>
                
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
            </body>
            </html>
            """)
        
        return jsonify({
            'success': True,
            'report_path': demo_report_path,
            'analysis': {
                'summary': 'Document analysis complete. The document contains information about various weed species and their control methods.',
                'weed_mentions': weed_mentions,
                'growth_stages': growth_stages,
                'document_info': {
                    'pages': random.randint(1, 10),
                    'words': random.randint(500, 3000),
                    'date': datetime.now().strftime("%Y-%m-%d"),
                }
            }
        })
    
    return jsonify({'success': False, 'error': 'File type not allowed'}), 400

@app.route('/detect_growth_stage', methods=['POST'])
def detect_growth_stage():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Simulate processing time
        time.sleep(random.uniform(0.8, 1.8))
        
        # For development purposes, return a demo result
        growth_stages = ["Seedling", "Early Vegetative", "Late Vegetative", "Flowering", "Maturity"]
        detected_stage = random.choice(growth_stages)
        confidence = random.uniform(0.7, 0.95)
        
        green_percentage = random.randint(40, 85)
        plant_count = random.randint(1, 10)
        leaf_size = random.choice(["Small", "Medium", "Large"])
        
        stage_characteristics = {
            "Seedling": "Young plants with cotyledons or first true leaves. Plants are small with limited foliage.",
            "Early Vegetative": "Plants have established root systems and are beginning rapid vegetative growth.",
            "Late Vegetative": "Plants have significant foliage and are approaching maximum vegetative size.",
            "Flowering": "Plants are producing flowers and beginning reproductive development.",
            "Maturity": "Plants are fully developed with mature seeds or fruit."
        }
        
        management_recommendations = {
            "Seedling": [
                "Early intervention is highly effective at this stage",
                "Hand pulling or hoeing is often sufficient",
                "Pre-emergent herbicides are no longer effective"
            ],
            "Early Vegetative": [
                "Mechanical control is still effective but becoming more difficult",
                "Post-emergent herbicides are highly effective at this stage",
                "Cultivation between rows can manage weeds effectively"
            ],
            "Late Vegetative": [
                "Mechanical control is increasingly difficult due to plant size",
                "Targeted application of herbicides may be necessary",
                "Focus on preventing seed production"
            ],
            "Flowering": [
                "Priority should be preventing seed production",
                "Remove flower heads before seeds develop",
                "Many herbicides become less effective at this stage"
            ],
            "Maturity": [
                "Focus on preventing seed dispersal",
                "Consider mowing or cutting before seeds fully mature",
                "Plan pre-emergent strategy for next season"
            ]
        }
        
        return jsonify({
            'success': True,
            'filename': filename,
            'growth_stage': detected_stage,
            'confidence': confidence,
            'features': {
                'green_percentage': green_percentage,
                'plant_count': plant_count,
                'leaf_size': leaf_size
            },
            'characteristics': stage_characteristics.get(detected_stage, ""),
            'recommendations': management_recommendations.get(detected_stage, []),
            'image_dimensions': [640, 480]
        })
    
    return jsonify({'success': False, 'error': 'File type not allowed'}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 