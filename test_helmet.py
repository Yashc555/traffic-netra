import cv2
import numpy as np
from models.yolo_detector import ViolationDetector
from utils.rules_engine import RulesEngine

def test_helmet():
    img_path = r"test_images\no_helmet.jpg"
    img = cv2.imread(img_path)
    if img is None:
        print("Failed to read image")
        return
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    detector = ViolationDetector()
    rules = RulesEngine()
    
    detections = detector.detect(img)
    violations = rules.evaluate(detections, active_checks={"No Helmet": True, "Triple Riding": True})
    
    print("Violations found:")
    for v in violations:
        print(f" - {v['label']} (Conf: {v['confidence']:.2f})")
    
    if not violations:
        print("No violations detected.")

if __name__ == "__main__":
    test_helmet()
