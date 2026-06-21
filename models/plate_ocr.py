"""
models/plate_ocr.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
License plate region extraction and OCR text normalisation.
Primary engine: PaddleOCR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import re
import cv2
import numpy as np
from typing import List, Dict, Optional


# ─── Character confusion map (hallucination correction) ────────────────────────
CHAR_CORRECTIONS = {
    "O": "0", "I": "1", "l": "1", "S": "5",
    "B": "8", "G": "6", "Z": "2", "D": "0",
    "0": "O", "1": "I",
}

# Canonical Indian number plate pattern: XX 00 XX 0000
_PLATE_REGEX = re.compile(
    r"([A-Z]{2})\s*(\d{1,2})\s*([A-Z]{1,3})\s*(\d{1,4})",
    re.IGNORECASE,
)


class PlateOCR:
    """Extracts and normalises licence plate text using PaddleOCR."""

    def __init__(self):
        self.ocr = None
        self.easy_ocr = None
        self._try_load_paddleocr()
        if self.ocr is None:
            self._try_load_easyocr()

    def _try_load_paddleocr(self):
        """Initialise the PaddleOCR engine."""
        try:
            from paddleocr import PaddleOCR
            # Add enable_mkldnn=False to bypass the OneDNN instruction crash
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang='en',
                enable_mkldnn=False  # <-- Add this flag
            )
            print("[TrafficNetra] PaddleOCR initialised successfully")
        except Exception as e:
            print(f"[TrafficNetra] PaddleOCR unavailable ({e}). OCR fallback active.")

    def _try_load_easyocr(self):
        """Initialise the EasyOCR engine as fallback."""
        try:
            import easyocr
            self.easy_ocr = easyocr.Reader(['en'])
            print("[TrafficNetra] EasyOCR initialised successfully")
        except Exception as e:
            print(f"[TrafficNetra] EasyOCR unavailable ({e}).")
        # ── Public API ─────────────────────────────────────────────────────────────

    def extract(self, image: np.ndarray, detections: List[Dict]) -> Optional[str]:
        """
        Locate license_plate boxes, crop, run OCR, and return best match.
        Now includes diagnostic logging.
        """
        plate_dets = [d for d in detections if d["class"] == "license_plate"]
        
        print(f"\n[DEBUG-OCR] Stage 1: YOLO found {len(plate_dets)} license plate bounding box(es).")

        if not plate_dets or (self.ocr is None and self.easy_ocr is None):
            return None

        best_text = None
        best_conf = 0.0

        for i, det in enumerate(plate_dets):
            x1, y1, x2, y2 = det["bbox"]
            print(f"[DEBUG-OCR] --- Processing Plate Crop {i+1} ---")
            print(f"[DEBUG-OCR] BBox Coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
            
            pad = 12
            h, w = image.shape[:2]
            cx1 = max(0, int(x1) - pad); cy1 = max(0, int(y1) - pad)
            cx2 = min(w, int(x2) + pad); cy2 = min(h, int(y2) + pad)

            crop = image[cy1:cy2, cx1:cx2]
            if crop.size == 0:
                print("[DEBUG-OCR] Error: Crop size is 0. Skipping.")
                continue

            if self.ocr is not None:
                text, conf = self._run_paddle(crop)
            else:
                text, conf = self._run_easyocr(crop)
            
            if text and conf > best_conf:
                best_text = text
                best_conf = conf

        print(f"[DEBUG-OCR] Final OCR Result chosen: {best_text} (Conf: {best_conf:.2f})\n")
        return best_text

    def _run_easyocr(self, crop: np.ndarray):
        """Preprocess crop and run EasyOCR safely."""
        h, w = crop.shape[:2]
        
        if h < 10 or w < 10:
            print(f"[DEBUG-OCR] Stage 2: Crop too small ({w}x{h}). EasyOCR aborted.")
            return None, 0.0

        resized = cv2.resize(crop, (w * 2, h * 2), interpolation=cv2.INTER_LINEAR)
        
        try:
            result = self.easy_ocr.readtext(resized)
            
            if not result:
                print("[DEBUG-OCR] Stage 2: EasyOCR ran but returned NO text.")
                return None, 0.0

            raw_parts = []
            conf_total = 0.0
            valid_lines = 0
            
            for line in result:
                if len(line) >= 3:
                    text = str(line[1])
                    conf = float(line[2])
                else:
                    continue

                if text.strip():
                    raw_parts.append(text.upper().strip())
                    conf_total += conf
                    valid_lines += 1

            if not raw_parts:
                print("[DEBUG-OCR] Stage 2: EasyOCR failed to extract valid characters.")
                return None, 0.0

            raw = "".join(raw_parts)
            avg_conf = conf_total / valid_lines
            
            print(f"[DEBUG-OCR] Stage 2: Raw Text from EasyOCR: '{raw}'")
            
            normalised = self._normalise(raw)
            print(f"[DEBUG-OCR] Stage 3: Regex Normalization Output: '{normalised}'")
            
            return normalised, avg_conf

        except Exception as e:
            print(f"[DEBUG-OCR] EasyOCR parsing error: {e}")
            return None, 0.0

    def _run_paddle(self, crop: np.ndarray):
        """Preprocess crop and run PaddleOCR safely."""
        h, w = crop.shape[:2]
        
        if h < 10 or w < 10:
            print(f"[DEBUG-OCR] Stage 2: Crop too small ({w}x{h}). PaddleOCR aborted.")
            return None, 0.0

        resized = cv2.resize(crop, (w * 2, h * 2), interpolation=cv2.INTER_LINEAR)
        
        try:
            result = self.ocr.ocr(resized)
            
            if not result or not result[0]:
                print("[DEBUG-OCR] Stage 2: PaddleOCR ran but returned NO text.")
                return None, 0.0

            raw_parts = []
            conf_total = 0.0
            valid_lines = 0
            
            for item in result:
                # Handle dict format (newer PaddleOCR/PaddleX)
                if isinstance(item, dict) and 'rec_texts' in item:
                    rec_texts = item.get('rec_texts', [])
                    rec_scores = item.get('rec_scores', [])
                    for i, text in enumerate(rec_texts):
                        if text and text.strip():
                            conf = rec_scores[i] if i < len(rec_scores) else 0.5
                            raw_parts.append(text.upper().strip())
                            conf_total += conf
                            valid_lines += 1
                # Handle old list of lists format
                elif isinstance(item, list):
                    for line in item:
                        if not isinstance(line, list) or len(line) < 2:
                            continue
                        data = line[1]
                        if isinstance(data, (tuple, list)):
                            text = str(data[0]) if data[0] else ""
                            conf = float(data[1]) if len(data) > 1 else 0.0
                        elif isinstance(data, str):
                            text = data
                            conf = 0.50
                        else:
                            continue

                        if text.strip():
                            raw_parts.append(text.upper().strip())
                            conf_total += conf
                            valid_lines += 1

            if not raw_parts:
                print("[DEBUG-OCR] Stage 2: PaddleOCR failed to extract valid characters.")
                return None, 0.0

            raw = "".join(raw_parts)
            avg_conf = conf_total / valid_lines
            
            print(f"[DEBUG-OCR] Stage 2: Raw Text from Paddle: '{raw}'")
            
            normalised = self._normalise(raw)
            print(f"[DEBUG-OCR] Stage 3: Regex Normalization Output: '{normalised}'")
            
            return normalised, avg_conf

        except Exception as e:
            print(f"[DEBUG-OCR] Parsing error: {e}")
            return None, 0.0
                
    def _normalise(self, raw: str) -> Optional[str]:
        """
        Clean the raw string, apply regex for Indian plates, 
        and correct common digit/letter confusions.
        """
        if not raw:
            return None

        # Strip EVERYTHING that is not an uppercase letter or a digit
        cleaned = re.sub(r'[^A-Z0-9]', '', raw.upper())

        # Try to match the strict standard plate pattern
        match = _PLATE_REGEX.search(cleaned)
        if match:
            state, dist, alpha, num = match.groups()
            state = _fix_alpha(state)
            alpha = _fix_alpha(alpha)
            num   = _fix_numeric(num)
            return f"{state} {dist.zfill(2)} {alpha} {num.zfill(4)}"

        # Fallback: If it's at least 6 characters, ends in a number, and has at least 2 letters
        if len(cleaned) >= 6 and cleaned[-1].isdigit() and sum(c.isalpha() for c in cleaned) >= 2:
            return cleaned[:10]

        return None


# ─── Segment-level Normalisation Helpers ─────────────────────────────────────

def _fix_alpha(text: str) -> str:
    """Correct digit→letter confusion in alphabetic segments."""
    mapping = {"0": "O", "1": "I", "5": "S", "8": "B", "6": "G"}
    return "".join(mapping.get(c, c) for c in text.upper())


def _fix_numeric(text: str) -> str:
    """Correct letter→digit confusion in numeric segments."""
    mapping = {"O": "0", "I": "1", "S": "5", "B": "8", "G": "6",
               "Z": "2", "D": "0", "Q": "0", "L": "1"}
    return "".join(mapping.get(c, c) for c in text.upper())