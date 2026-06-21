#!/usr/bin/env python3
"""
train.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fine-tuning pipeline for Traffic Netra YOLOv8 models.
Supports training on custom datasets or generating a synthetic
dataset for testing/demonstration purposes.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import argparse
import yaml
import cv2
import numpy as np
import random
from ultralytics import YOLO

def generate_synthetic_dataset(output_dir="synthetic_dataset", num_train=20, num_val=5, img_size=256):
    """
    Generates a synthetic dataset of shapes to verify the fine-tuning pipeline.
    Class 0: helmet (represented by a blue circle)
    Class 1: no_helmet (represented by a red circle)
    Class 2: license_plate (represented by a yellow rectangle)
    """
    print(f"[TrafficNetra] Generating synthetic dataset in '{output_dir}'...")
    
    dirs = {
        "train_img": os.path.join(output_dir, "images", "train"),
        "val_img": os.path.join(output_dir, "images", "val"),
        "train_lbl": os.path.join(output_dir, "labels", "train"),
        "val_lbl": os.path.join(output_dir, "labels", "val"),
    }
    
    for path in dirs.values():
        os.makedirs(path, exist_ok=True)
        
    def generate_split(num_images, img_dir, lbl_dir):
        for i in range(num_images):
            # Create a dark gray background image
            img = np.zeros((img_size, img_size, 3), dtype=np.uint8)
            img += np.random.randint(15, 45, (img_size, img_size, 3), dtype=np.uint8)
            
            num_objects = random.randint(1, 4)
            labels = []
            
            for _ in range(num_objects):
                class_id = random.choice([0, 1, 2])
                
                if class_id in (0, 1): # Helmet or No Helmet (Circle)
                    r = random.randint(15, 30)
                    cx = random.randint(r + 10, img_size - r - 10)
                    cy = random.randint(r + 10, img_size - r - 10)
                    
                    # Blue for helmet (0), Red for no_helmet (1)
                    color = (255, 0, 0) if class_id == 0 else (0, 0, 255)
                    cv2.circle(img, (cx, cy), r, color, -1)
                    
                    # YOLO format: class_id, x_center, y_center, width, height (normalized)
                    nx = cx / img_size
                    ny = cy / img_size
                    nw = (2 * r) / img_size
                    nh = (2 * r) / img_size
                
                else: # License Plate (Rectangle)
                    rw = random.randint(40, 70)
                    rh = random.randint(15, 30)
                    cx = random.randint(rw//2 + 10, img_size - rw//2 - 10)
                    cy = random.randint(rh//2 + 10, img_size - rh//2 - 10)
                    
                    # Yellow for license_plate (BGR: 0, 255, 255)
                    cv2.rectangle(img, (cx - rw//2, cy - rh//2), (cx + rw//2, cy + rh//2), (0, 255, 255), -1)
                    
                    nx = cx / img_size
                    ny = cy / img_size
                    nw = rw / img_size
                    nh = rh / img_size
                
                labels.append(f"{class_id} {nx:.6f} {ny:.6f} {nw:.6f} {nh:.6f}")
                
            # Save image
            img_path = os.path.join(img_dir, f"img_{i}.jpg")
            cv2.imwrite(img_path, img)
            
            # Save label file
            lbl_path = os.path.join(lbl_dir, f"img_{i}.txt")
            with open(lbl_path, "w") as f:
                f.write("\n".join(labels))
                
    generate_split(num_train, dirs["train_img"], dirs["train_lbl"])
    generate_split(num_val, dirs["val_img"], dirs["val_lbl"])
    
    # Write dataset config
    data_config = {
        "path": os.path.abspath(output_dir),
        "train": "images/train",
        "val": "images/val",
        "names": {
            0: "helmet",
            1: "no_helmet",
            2: "license_plate"
        }
    }
    
    yaml_path = os.path.join(output_dir, "dataset.yaml")
    with open(yaml_path, "w") as f:
        yaml.safe_dump(data_config, f, default_flow_style=False)
        
    print(f"[TrafficNetra] Synthetic dataset created at: {yaml_path}")
    return yaml_path

def main():
    parser = argparse.ArgumentParser(description="Fine-tune YOLOv8 models for Traffic Netra")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Path to base model (e.g., yolov8n.pt)")
    parser.add_argument("--data", type=str, default=None, help="Path to dataset.yaml (if omitted, synthetic data is generated)")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=8, help="Training batch size")
    parser.add_argument("--imgsz", type=int, default=256, help="Image size for training")
    parser.add_argument("--device", type=str, default="cpu", help="Device to train on (e.g. cpu, mps, cuda)")
    
    args = parser.parse_args()
    
    # Initialize / Download base model if it doesn't exist
    print(f"[TrafficNetra] Loading model: {args.model}")
    model = YOLO(args.model)
    
    # Determine dataset config
    if args.data is None:
        print("[TrafficNetra] No dataset.yaml provided. Falling back to synthetic dataset.")
        data_yaml = generate_synthetic_dataset()
    else:
        data_yaml = args.data
        if not os.path.exists(data_yaml):
            raise FileNotFoundError(f"Provided dataset config not found: {data_yaml}")
            
    print(f"[TrafficNetra] Starting training on {data_yaml} for {args.epochs} epochs (batch size: {args.batch}, resolution: {args.imgsz})")
    
    # Execute fine-tuning
    results = model.train(
        data=data_yaml,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        project="runs/detect",
        name="fine_tune_yolo"
    )
    
    print("\n[TrafficNetra] Fine-tuning finished successfully!")
    print(f"Results saved under: runs/fine_tune_yolo")

if __name__ == "__main__":
    main()
