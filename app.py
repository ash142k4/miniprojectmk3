import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from app.utils.weed_detector import WeedDetector
from app.utils.report_generator import generate_report
from app.utils.document_analyzer import analyze_document

app = Flask(__name__, 
            static_folder='app/static',
            template_folder='app/templates')

app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.secret_key = 'weed_detection_app_secret_key'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('app/static/reports', exist_ok=True)

# Initialize the weed detector
detector = WeedDetector()

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
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image with YOLOv8
        results = detector.detect(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'results': results
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['document']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze the document
        analysis_results = analyze_document(filepath)
        
        # Generate a report
        report_path = generate_report(analysis_results)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'report_path': report_path,
            'analysis': analysis_results
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/detect_growth_stage', methods=['POST'])
def detect_growth_stage():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Detect the growth stage
        growth_stage = detector.detect_growth_stage(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'growth_stage': growth_stage
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True) 