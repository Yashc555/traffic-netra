# inference_server.py
"""
TrafficNetra Local Inference API Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Runs the heavy YOLOv8 + PaddleOCR models on the local machine,
allowing a lightweight frontend to run securely in the cloud.
"""

import os
import sys
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form
import uvicorn

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from models.yolo_detector import ViolationDetector
from models.plate_ocr import PlateOCR
from utils.image_filters import ImagePreprocessor
from utils.rules_engine import RulesEngine

app = FastAPI(
    title="TrafficNetra Inference Server",
    description="Heavy model inference execution endpoint for YOLOv8 & OCR"
)

# Initialize engines on startup
print("[TrafficNetra Server] Initializing engines...")
detector = ViolationDetector()
ocr_engine = PlateOCR()
preprocessor = ImagePreprocessor()
rules_engine = RulesEngine()
print("[TrafficNetra Server] All engines loaded and ready!")

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    triple_riding: str = Form("true"),
    helmet_compliance: str = Form("true")
):
    """
    Accepts an image file and active checks, runs the inference pipeline,
    and returns detections, violations, and extracted registration numbers.
    """
    # Parse incoming parameters
    active_checks = {
        "Triple Riding": triple_riding.lower() == "true",
        "No Helmet": helmet_compliance.lower() == "true"
    }

    # Read image contents
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert BGR to RGB (required by detector)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # 1. Enhance Contrast / Brightness
    img_enhanced = preprocessor.auto_enhance(img_rgb)

    # 2. Run Object Detection (YOLOv8)
    detections = detector.detect(img_enhanced, active_checks=active_checks)

    # 3. Evaluate Traffic Rules
    violations = rules_engine.evaluate(detections, active_checks=active_checks)

    # 4. Extract License Plate OCR
    plate_text = ocr_engine.extract(img_enhanced, detections)

    return {
        "detections": detections,
        "violations": violations,
        "plate_text": plate_text
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
