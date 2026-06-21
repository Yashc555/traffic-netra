import sys
import os
import cv2
from models.yolo_detector import ViolationDetector
from models.plate_ocr import PlateOCR

def test_ocr():
    img_path = r"test_images/no_violation_number_plate_visible.png"
    img = cv2.imread(img_path)
    if img is None:
        print("Failed to read image")
        return
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    detector = ViolationDetector()
    ocr = PlateOCR()
    
    detections = detector.detect(img)
    print("Detections:", detections)
    
    plate_text = ocr.extract(img, detections)
    print("Extracted Plate:", plate_text)

if __name__ == "__main__":
    test_ocr()
