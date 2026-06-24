# Traffic Netra Dashboard V2

Automated Traffic Violation Detection Dashboard

Traffic Netra is a Streamlit based web application designed for automated traffic enforcement. It processes images, detects vehicles, persons, and traffic infrastructure, applies traffic rule logic to flag violations, performs OCR on license plates, and generates a downloadable PDF evidence report. This project was developed as a hackathon project focusing on Computer Vision and Traffic Enforcement.

## Features

* Object Detection: Utilizes Ultralytics YOLOv8 to detect vehicles (cars, motorcycles), persons, helmets, and traffic infrastructure like stop lines.
* Violation Rules Engine: Evaluates geometric and spatial logic on bounding boxes to detect violations such as:
  * Triple Riding (e.g., 3 people on one motorcycle)
  * No Helmet
  * Stop Line Violations
  * Illegal Parking
* License Plate Recognition (OCR): Integrates PaddleOCR (with EasyOCR fallback) to extract text from detected license plates, validating Indian vehicle registration formats using Regex.
* Image Preprocessing: Automatically enhances contrast and brightness of uploaded images before analysis.
* Automated Reporting: Generates a court admissible PDF document containing the original image, cropped evidence of the violation, and metadata using fpdf2.
* Interactive UI: Built purely with Python using Streamlit, featuring custom CSS styling and SVG icons.

## Technical Architecture

* Frontend / Web Server: Streamlit (Runs by default on port 8501)
* Computer Vision (Object Detection): OpenCV, YOLOv8 (ultralytics)
* Optical Character Recognition (OCR): PaddleOCR, EasyOCR
* Image Processing: Pillow (PIL), NumPy
* PDF Generation: fpdf2

### Pipeline Flow

1. Preprocessing: Image contrast and brightness are enhanced (utils/image_filters.py).
2. Detection: YOLOv8 scans the image, returning bounding boxes for targets (models/yolo_detector.py).
3. Rule Evaluation: Bounding boxes are analyzed by the Rules Engine to confirm violations (utils/rules_engine.py).
4. Annotation: Confirmed violations are highlighted with bounding boxes directly on the image.
5. OCR: License plates are extracted and read (models/plate_ocr.py).
6. Report Generation: A PDF containing all evidence and metadata is compiled for download (utils/report_gen.py).

## Project Structure

* app.py: Main Streamlit application and entry point. Handles UI layout, routing, state management, and inference pipeline orchestration.
* ui_assets.py: Custom CSS and SVG styling to override Streamlit defaults.
* models/
  * yolo_detector.py: YOLOv8 model wrapper for object detection.
  * plate_ocr.py: PaddleOCR wrapper for license plate reading.
* utils/
  * image_filters.py: Image enhancement and preprocessing logic.
  * rules_engine.py: Core logic for determining traffic violations based on spatial data.
  * report_gen.py: Dynamic PDF report compilation.
* requirements.txt: Python dependency list.

## Building & Running Instructions

### Prerequisites
* Python 3.9+
* Git

### Installation

1. Navigate to the project directory:
   ```bash
   cd path/to/TrafficNetraDashboard/V2
   ```

2. Create a virtual environment (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: YOLOv8 model weights will be downloaded automatically on the first run.*

### Running the Application

To start the Traffic Netra dashboard locally, run the following command from the root directory:

```bash
streamlit run app.py
```

The application will start the built in web server. Open your browser and navigate to the local URL provided in the terminal (typically http://localhost:8501) to access the dashboard.
