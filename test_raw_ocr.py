import cv2
import numpy as np
from paddleocr import PaddleOCR

def test_raw_paddle():
    ocr = PaddleOCR(use_angle_cls=True, lang='en', enable_mkldnn=False)
    img_path = r"test_images\no_violation_number_plate_visible.png"
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Coordinates from logs
    x1, y1, x2, y2 = 384, 442, 444, 458
    pad = 12
    h, w = img.shape[:2]
    cx1 = max(0, int(x1) - pad); cy1 = max(0, int(y1) - pad)
    cx2 = min(w, int(x2) + pad); cy2 = min(h, int(y2) + pad)

    crop = img[cy1:cy2, cx1:cx2]
    
    # Resize as in PlateOCR
    h_c, w_c = crop.shape[:2]
    resized = cv2.resize(crop, (w_c * 2, h_c * 2), interpolation=cv2.INTER_LINEAR)
    
    # cv2.imwrite('debug_crop.png', resized) # just to see what we are passing
    
    result = ocr.ocr(resized)
    print("RAW RESULT:", result)

if __name__ == "__main__":
    test_raw_paddle()
