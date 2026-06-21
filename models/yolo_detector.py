"""
models/yolo_detector.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOLOv8 perception wrapper for Traffic Netra.
Handles model loading, inference, demo-mode mock detections,
and bounding-box annotation rendering.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import cv2
import numpy as np
from typing import List, Dict, Optional, Any

# ─── COCO class IDs we care about ─────────────────────────────────────────────
COCO_RELEVANT = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}

# ─── Visual Style ──────────────────────────────────────────────────────────────
LABEL_COLORS = {
    "person":        (52,  152, 219),   # blue
    "motorcycle":    (46,  204, 113),   # green
    "car":           (52,  152, 219),   # blue
    "truck":         (52,  152, 219),
    "bus":           (52,  152, 219),
    "bicycle":       (46,  204, 113),
    "license_plate": (241, 196,  15),   # yellow
    "helmet":        (39,  174,  96),
    "no_helmet":     (231,  76,  60),   # red
    "VIOLATION":     (192,  57,  43),   # deep red
}


def _compute_iou(box_a, box_b) -> float:
    """Compute IoU between two [x1, y1, x2, y2] boxes."""
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)

    inter_w = max(0, ix2 - ix1)
    inter_h = max(0, iy2 - iy1)
    inter_area = inter_w * inter_h

    area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    area_b = max(0, bx2 - bx1) * max(0, by2 - by1)
    union = area_a + area_b - inter_area

    return (inter_area / union) if union > 0 else 0.0



from huggingface_hub import hf_hub_download

class ViolationDetector:
    """
    Wraps YOLOv8 for traffic violation detection.
    Loads standard COCO, plus custom Helmet and License Plate models.
    """

    def __init__(self, base_model_path: str = "yolov8n.pt", load_models: bool = True):
        self.base_model   = None
        self.helmet_model = None
        self.plate_model  = None
        if load_models:
            self._try_load_models(base_model_path)

    def _try_load_models(self, base_model_path):
        """Load all three models. Uses huggingface_hub to fetch custom weights."""
        try:
            from ultralytics import YOLO
            
            # 1. Base Model (Cars, Persons, Motorcycles)
            print(f"[TrafficNetra] Loading Base YOLOv8: {base_model_path}")
            self.base_model = YOLO(base_model_path)
            
            # 2. Helmet Model
            print("[TrafficNetra] Downloading/Loading Helmet Model...")
            helmet_path = hf_hub_download(repo_id="JarvanLee/yolov8-helmet-violation-detection", filename="weights/best.pt")
            self.helmet_model = YOLO(helmet_path)
            
            # 3. License Plate Model
            print("[TrafficNetra] Downloading/Loading Plate Model...")
            plate_path = hf_hub_download(repo_id="Koushim/yolov8-license-plate-detection", filename="best.pt")
            self.plate_model = YOLO(plate_path)

        except Exception as e:
            print(f"[TrafficNetra] Models not available ({e}). Demo mode active.")
            self.base_model = None

    def detect(
        self,
        image: np.ndarray,
        active_checks: dict     = None,
        conf_threshold: float   = 0.35,
        iou_threshold: float    = 0.45,
    ) -> List[Dict[str, Any]]:
        """
        Run detection on image.
        Returns list of detection dicts.
        """
        h, w = image.shape[:2]

        if self.base_model is None: 
            return []

        return self._run_yolo(image, h, w, conf_threshold, iou_threshold)
    
    def annotate(
        self,
        image: np.ndarray,
        detections: List[Dict],
        violations: List[Dict],
    ) -> np.ndarray:
        """
        Draw bounding boxes, labels, and violation overlays on image.
        Returns annotated numpy array (BGR→RGB).
        """
        img = image.copy()
        h, w = img.shape[:2]

        # Collect violation labels for highlight
        violation_labels = {v["label"] for v in violations}

        # ── Semi-transparent overlay for violations ────────────────────────
        overlay = img.copy()

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            cls   = det["class"]
            conf  = det["confidence"]
            color = LABEL_COLORS.get(cls, (150, 150, 150))

            is_violation_box = cls in ("no_helmet", "VIOLATION", "no_parking_zone") or \
                               (cls == "stop_line")

            # Fill for violation boxes
            if is_violation_box:
                cv2.rectangle(overlay, (x1, y1), (x2, y2), (192, 57, 43), -1)
            # Fill transparent for detected objects
            else:
                cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)

        # Blend overlay
        img = cv2.addWeighted(overlay, 0.12, img, 0.88, 0)

        # ── Draw boxes and labels ──────────────────────────────────────────
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            cls   = det["class"]
            conf  = det["confidence"]
            color = LABEL_COLORS.get(cls, (150, 150, 150))

            thickness = 2

            # Special styling for stop line / zones
            if cls == "stop_line":
                cv2.line(img, (x1, (y1+y2)//2), (x2, (y1+y2)//2),
                         (255, 50, 50), 3)
                cv2.putText(img, "STOP LINE", (x1+8, (y1+y2)//2 - 8),
                            cv2.FONT_HERSHEY_DUPLEX, 0.55, (255, 50, 50), 1, cv2.LINE_AA)
                continue

            if cls == "no_parking_zone":
                pts = np.array([[x1,y1],[x2,y1],[x2,y2],[x1,y2]], np.int32)
                cv2.polylines(img, [pts], True, (255, 100, 50), 2, cv2.LINE_AA)
                _draw_dashed_rect(img, x1, y1, x2, y2, (255, 100, 50))
                continue

            # Standard bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness, cv2.LINE_AA)

            # Corner accents
            _draw_corner_accents(img, x1, y1, x2, y2, color, size=14, thick=3)

            # Label background
            label_txt = f"{cls.replace('_', ' ').upper()}  {conf:.0%}"
            (tw, th), _ = cv2.getTextSize(label_txt, cv2.FONT_HERSHEY_DUPLEX, 0.45, 1)
            lx1, ly1 = x1, max(0, y1 - th - 10)
            lx2, ly2 = x1 + tw + 12, y1

            cv2.rectangle(img, (lx1, ly1), (lx2, ly2), color, -1)
            cv2.putText(img, label_txt, (lx1+6, ly2-4),
                        cv2.FONT_HERSHEY_DUPLEX, 0.45, (255,255,255), 1, cv2.LINE_AA)

        # ── Violation banner at top ────────────────────────────────────────
        if violations:
            banner_h = 36
            cv2.rectangle(img, (0, 0), (w, banner_h), (192, 57, 43), -1)
            v_text = "VIOLATION DETECTED: " + "  |  ".join(v["label"].upper() for v in violations)
            cv2.putText(img, v_text, (12, 24),
                        cv2.FONT_HERSHEY_DUPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)

        # ── Watermark ─────────────────────────────────────────────────────
        wm_text = "TRAFFIC NETRA — AI EVIDENCE"
        (ww, wh), _ = cv2.getTextSize(wm_text, cv2.FONT_HERSHEY_DUPLEX, 0.4, 1)
        cv2.putText(img, wm_text, (w - ww - 10, h - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.4, (180, 170, 158), 1, cv2.LINE_AA)

        return img

    # ── Private Helpers ────────────────────────────────────────────────────────

    def _run_yolo(
        self,
        image: np.ndarray,
        h: int, w: int,
        conf_thr: float,
        iou_thr: float,
    ) -> List[Dict]:
        """Run all three YOLOv8 models and aggregate results."""
        detections = []
        
        # ── 1. Base Model (Vehicles & Persons) ──
        # We run the base model at a very low threshold to catch occluded riders, 
        # then apply class-specific thresholds.
        base_res = self.base_model.predict(source=image, conf=0.10, iou=iou_thr, verbose=False)
        for r in base_res:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                if cls_id in COCO_RELEVANT:
                    cls_name = COCO_RELEVANT[cls_id]
                    conf = float(box.conf[0])
                    
                    # Class-specific confidence thresholds
                    # Persons and Motorcycles are often occluded in triple-riding
                    min_conf = 0.15 if cls_name in ("person", "motorcycle") else conf_thr
                    
                    if conf >= min_conf:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        detections.append({
                            "class":      cls_name,
                            "bbox":       [x1, y1, x2, y2],
                            "bbox_n":     [x1/w, y1/h, x2/w, y2/h],
                            "confidence": conf,
                        })

        # ── 2. Helmet Model ──
        helmet_res = self.helmet_model.predict(source=image, conf=0.3, iou=iou_thr, verbose=False)
        for r in helmet_res:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                raw_name = r.names[cls_id].lower()
                
                # Standardise the output name for our RulesEngine
                # Usually these models output 'with_helmet', 'without_helmet', 'head', 'helmet'
                mapped_name = "no_helmet" if ("without" in raw_name or "no" in raw_name or raw_name == "head") else "helmet"
                
                # Ignore the person class from the helmet model since base model handles it better
                if raw_name == "person":
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "class":      mapped_name,
                    "bbox":       [x1, y1, x2, y2],
                    "bbox_n":     [x1/w, y1/h, x2/w, y2/h],
                    "confidence": float(box.conf[0]),
                })

        # ── 3. License Plate Model ──
        plate_res = self.plate_model.predict(source=image, conf=conf_thr, iou=iou_thr, verbose=False)
        for r in plate_res:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "class":      "license_plate",
                    "bbox":       [x1, y1, x2, y2],
                    "bbox_n":     [x1/w, y1/h, x2/w, y2/h],
                    "confidence": float(box.conf[0]),
                })
        # ── Cleanup: Return all detections without removing person boxes ──
        return detections


# ─── Drawing Utilities ────────────────────────────────────────────────────────

def _draw_corner_accents(img, x1, y1, x2, y2, color, size=16, thick=3):
    """Draw stylish corner marks instead of full rectangle."""
    pts = [
        ((x1, y1+size), (x1, y1), (x1+size, y1)),
        ((x2-size, y1), (x2, y1), (x2, y1+size)),
        ((x1, y2-size), (x1, y2), (x1+size, y2)),
        ((x2-size, y2), (x2, y2), (x2, y2-size)),
    ]
    for p1, corner, p2 in pts:
        cv2.line(img, p1, corner, color, thick, cv2.LINE_AA)
        cv2.line(img, corner, p2, color, thick, cv2.LINE_AA)


def _draw_dashed_rect(img, x1, y1, x2, y2, color, dash=12, gap=8):
    """Draw a dashed rectangle border."""
    def dash_line(p1, p2):
        dx = p2[0]-p1[0]; dy = p2[1]-p1[1]
        length = max(abs(dx), abs(dy))
        if length == 0:
            return
        steps = int(length / (dash + gap))
        for i in range(steps):
            t0 = i * (dash + gap) / length
            t1 = min(1.0, t0 + dash / length)
            pa = (int(p1[0] + t0*dx), int(p1[1] + t0*dy))
            pb = (int(p1[0] + t1*dx), int(p1[1] + t1*dy))
            cv2.line(img, pa, pb, color, 1, cv2.LINE_AA)

    dash_line((x1,y1),(x2,y1))
    dash_line((x2,y1),(x2,y2))
    dash_line((x2,y2),(x1,y2))
    dash_line((x1,y2),(x1,y1))
