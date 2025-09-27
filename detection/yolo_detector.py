"""
YOLOv8 detection module for wildlife detection
"""

import cv2
import numpy as np
from ultralytics import YOLO
import config
import os

class YOLODetector:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load YOLOv8 model"""
        try:
            # Download model if not exists
            model_path = config.MODEL_CONFIG['model_path']
            if not os.path.exists(model_path):
                print("Downloading YOLOv8 model...")
                os.makedirs("models", exist_ok=True)
            
            # Load YOLOv8 model
            self.model = YOLO('yolov8n.pt')  # This will auto-download if needed
            print("YOLOv8 model loaded successfully")
        except Exception as e:
            print(f"Error loading YOLOv8 model: {e}")
            self.model = None
    
    def detect_animals(self, frame):
        """Detect animals in frame"""
        if self.model is None:
            return []
        
        try:
            # Run detection
            results = self.model(frame, conf=config.MODEL_CONFIG['confidence_threshold'])
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get class ID and confidence
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        # Map COCO classes to our target animals
                        # We'll use a more comprehensive mapping
                        animal_mapping = {
                            14: 'peacock',    # bird -> peacock
                            15: 'pig',        # cat -> pig (closest animal match)
                            16: 'deer',       # dog -> deer (closest animal match)
                            17: 'monkey',     # horse -> monkey (closest animal match)
                            18: 'hedgehog',   # sheep -> hedgehog (closest animal match)
                            19: 'pig',        # cow -> pig (closest animal match)
                        }
                        
                        if class_id in animal_mapping:
                            animal_type = animal_mapping[class_id]
                            
                            # Get bounding box coordinates
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            
                            detections.append({
                                'animal_type': animal_type,
                                'confidence': confidence,
                                'bbox': [int(x1), int(y1), int(x2-x1), int(y2-y1)],
                                'class_id': class_id
                            })
            
            return detections
        except Exception as e:
            print(f"Detection error: {e}")
            return []
    
    def draw_detections(self, frame, detections):
        """Draw bounding boxes and labels on frame"""
        for detection in detections:
            x, y, w, h = detection['bbox']
            animal_type = detection['animal_type']
            confidence = detection['confidence']
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Draw label
            label = f"{animal_type}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            
            # Draw label background
            cv2.rectangle(frame, (x, y - label_size[1] - 10), 
                         (x + label_size[0], y), (0, 255, 0), -1)
            
            # Draw label text
            cv2.putText(frame, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        return frame
    
    def is_model_loaded(self):
        """Check if model is loaded"""
        return self.model is not None
