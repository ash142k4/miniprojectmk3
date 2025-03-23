# WeedDetect Pro

A smart weed detection system that leverages YOLOv12 AI technology to identify and manage weeds in agricultural fields.

![WeedDetect Pro Logo](app/static/images/logo.png)

## About the Project

WeedDetect Pro is an academic project developed by students at DIT, Pimpri. This web application uses computer vision and deep learning to detect weed species, analyze growth stages, and provide management recommendations.

### Key Features

- **Weed Detection**: Identify weed species with detailed information and control methods
- **Growth Stage Analysis**: Determine plant development stages and receive tailored recommendations
- **Document Analysis**: Parse and analyze agricultural documents for insights
- **Modern Dashboard**: Professional UI with comprehensive analytics

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributors](#contributors)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Deployment](#deployment)

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.12+ (Python 3.12.6 recommended)
- pip (Python package manager)
- Git (optional, for cloning the repository)
- Web browser (Chrome/Firefox recommended)

## Installation

Follow these steps to set up the project locally:

### 1. Clone the repository or download the source code

```bash
git clone https://github.com/your-username/weeddetect-pro.git
cd weeddetect-pro
```

Or download and extract the ZIP file.

### 2. Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If no requirements.txt file exists, install the following packages:

```bash
pip install flask pillow numpy
```

### 4. Set up the directory structure

Ensure the following directories exist (create them if they don't):

```bash
mkdir -p app/static/uploads
mkdir -p app/static/reports
```

## Project Structure

```
weeddetect-pro/
├── app/
│   ├── models/           # YOLOv12 model files
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── main.js
│   │   ├── images/
│   │   │   └── logo.png
│   │   ├── uploads/
│   │   └── reports/
│   ├── templates/
│   │   ├── index.html
│   │   └── about.html
│   └── utils/            # Utility modules
├── run.py                # Main Flask application
├── app.py                # Alternative entry point
├── requirements.txt      # Python dependencies
└── README.md
```

## Running the Application

To start the WeedDetect Pro application:

```bash
python run.py
```

The application will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

To stop the application, press `CTRL+C` in the terminal where it's running.

## Usage

### Weed Detection

1. Navigate to the "Weed Detection" tab via the sidebar
2. Click on the upload area or drag and drop an image
3. The system will process the image and display detected weeds with detailed information
4. View characteristics, control methods, and environmental analysis

### Growth Stage Analysis

1. Navigate to the "Growth Stage" tab
2. Upload an image of plants/crops
3. Review the detected growth stage, characteristics, and management recommendations

### Document Analysis

1. Navigate to the "Document Analysis" tab
2. Upload an agricultural document (PDF/DOCX)
3. Review the extracted information, weed mentions, and recommendations
4. Download the detailed report if needed

## API Endpoints

The application provides the following RESTful API endpoints:

- `POST /upload_image` - Upload and process images for weed detection
- `POST /detect_growth_stage` - Detect plant growth stages from images
- `POST /upload_document` - Process and analyze agricultural documents

Detailed API documentation is available in the code comments.

## Contributors

### Students

- ASHUTOSH MORE
- HUSAIN DUDHIYAWALA
- NIKHIL THUBE
- KETAN THAKARE

### Project Guides

- MRS. APARNA KULKARNI
- MRS. SONALI SAWARDEKAR

## Institution

Department of Information Technology  
DIT, Pimpri  
Pune, Maharashtra

## Troubleshooting

### Common Issues

1. **Missing Directories**:
   If you encounter errors related to missing directories, ensure you've created all required directories:

   ```bash
   mkdir -p app/static/uploads app/static/reports
   ```

2. **Port Already in Use**:
   If port 5000 is already in use, you can modify the port in `run.py`:

   ```python
   if __name__ == '__main__':
       app.run(debug=True, port=5001)  # Change port number
   ```

3. **Module Import Errors**:
   Ensure your virtual environment is activated and all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

### Development

For developers who want to extend the application:

1. **Adding New Weed Classes**:

   - Add new weed class definitions in `run.py` in the `YOLOWeedDetector` class
   - Include scientific name, growth pattern, habitat, and remedy information

2. **Customizing the UI**:

   - Frontend styling is in `app/static/css/styles.css`
   - JavaScript functionality is in `app/static/js/main.js`
   - HTML templates are in `app/templates/`

3. **Integrating a Real YOLO Model**:
   - Replace the mock detection in `YOLOWeedDetector.detect()` with actual YOLO code
   - Add your trained model weights to the `app/models/` directory
   - Update the inference code to use the actual model

## Deployment

For deploying to a production environment:

1. Set `debug=False` in `run.py`
2. Use a production WSGI server like Gunicorn or uWSGI
3. Consider using a reverse proxy like Nginx

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "run:app"
```

---

&copy; 2023 DIT, Pimpri. All rights reserved.
