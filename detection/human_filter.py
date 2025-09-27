"""
Human Detection Filter to Prevent False Positives
"""

import cv2
import numpy as np
from ultralytics import YOLO

class HumanFilter:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        """Load YOLOv8 model for human detection"""
        try:
            self.model = YOLO('yolov8n.pt')
            print("Human filter model loaded successfully")
        except Exception as e:
            print(f"Error loading human filter model: {e}")
            self.model = None
    
    def is_human_present(self, frame, bbox):
        """Check if human is present in the given bounding box area"""
        if self.model is None:
            return False
        
        try:
            x1, y1, x2, y2 = bbox
            
            # Extract region of interest
            roi = frame[y1:y2, x1:x2]
            if roi.size == 0:
                return False
            
            # Run detection on the ROI
            results = self.model(roi, conf=0.5)
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        # Check for person (class 0)
                        if class_id == 0 and confidence > 0.6:
                            return True
            
            return False
            
        except Exception as e:
            print(f"Human filter error: {e}")
            return False
    
    def filter_human_detections(self, frame, detections):
        """Filter out detections that are likely humans"""
        filtered_detections = []
        
        for detection in detections:
            bbox = detection['bbox']
            x, y, w, h = bbox
            
            # Check if human is present in this area
            if not self.is_human_present(frame, [x, y, x+w, y+h]):
                filtered_detections.append(detection)
            else:
                print(f"🚫 Filtered out human detection: {detection['animal_type']}")
        
        return filtered_detections
    
    def get_human_regions(self, frame):
        """Get regions where humans are detected"""
        if self.model is None:
            return []
        
        human_regions = []
        
        try:
            results = self.model(frame, conf=0.6)
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        if class_id == 0:  # Person
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            human_regions.append({
                                'bbox': [int(x1), int(y1), int(x2-x1), int(y2-y1)],
                                'confidence': confidence
                            })
            
            return human_regions
            
        except Exception as e:
            print(f"Human region detection error: {e}")
            return []
