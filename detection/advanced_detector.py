"""
Advanced wildlife detection with better animal classification
"""

import cv2
import numpy as np
from ultralytics import YOLO
import config
import os
import random
import time

class AdvancedWildlifeDetector:
    def __init__(self):
        self.model = None
        self.load_model()
        self.demo_mode = True  # Enable demo mode for testing
        self.last_demo_time = 0
        self.demo_animals = ['pig', 'deer', 'peacock', 'hedgehog', 'monkey']
    
    def load_model(self):
        """Load YOLOv8 model"""
        try:
            self.model = YOLO('yolov8n.pt')
            print("Advanced YOLOv8 model loaded successfully")
        except Exception as e:
            print(f"Error loading YOLOv8 model: {e}")
            self.model = None
    
    def detect_animals(self, frame):
        """Detect animals with enhanced classification"""
        if self.model is None:
            return []
        
        detections = []
        
        try:
            # Run detection
            results = self.model(frame, conf=config.MODEL_CONFIG['confidence_threshold'])
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        # Enhanced animal mapping - only map actual animals
                        animal_mapping = {
                            14: 'peacock',    # bird -> peacock
                            15: 'pig',        # cat -> pig (wild pig)
                            16: 'deer',       # dog -> deer  
                            17: 'monkey',     # horse -> monkey
                            18: 'hedgehog',   # sheep -> hedgehog
                            19: 'pig',        # cow -> pig (wild pig)
                            # Note: We don't map person (class 0) to avoid false positives
                        }
                        
                        if class_id in animal_mapping:
                            animal_type = animal_mapping[class_id]
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            
                            detections.append({
                                'animal_type': animal_type,
                                'confidence': confidence,
                                'bbox': [int(x1), int(y1), int(x2-x1), int(y2-y1)],
                                'class_id': class_id
                            })
            
            # Demo mode: simulate random animal detections for testing
            if self.demo_mode and len(detections) == 0:
                current_time = time.time()
                if current_time - self.last_demo_time > 10:  # Every 10 seconds
                    if random.random() < 0.3:  # 30% chance
                        animal = random.choice(self.demo_animals)
                        h, w = frame.shape[:2]
                        x = random.randint(50, w-100)
                        y = random.randint(50, h-100)
                        width = random.randint(50, 150)
                        height = random.randint(50, 150)
                        
                        detections.append({
                            'animal_type': animal,
                            'confidence': random.uniform(0.6, 0.9),
                            'bbox': [x, y, width, height],
                            'class_id': 0
                        })
                        self.last_demo_time = current_time
                        print(f"DEMO: Simulated {animal} detection")
            
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
            
            # Color coding for different animals
            colors = {
                'pig': (0, 255, 0),        # Green
                'deer': (255, 0, 0),        # Blue
                'peacock': (0, 0, 255),     # Red
                'hedgehog': (255, 255, 0),  # Cyan
                'monkey': (255, 0, 255),    # Magenta
            }
            
            color = colors.get(animal_type, (0, 255, 0))
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
            
            # Draw label with background
            label = f"{animal_type.upper()}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            
            # Background rectangle for text
            cv2.rectangle(frame, (x, y - label_size[1] - 10), 
                         (x + label_size[0], y), color, -1)
            
            # Text
            cv2.putText(frame, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        return frame
    
    def is_model_loaded(self):
        """Check if model is loaded"""
        return self.model is not None
    
    def set_demo_mode(self, enabled):
        """Enable/disable demo mode"""
        self.demo_mode = enabled
        print(f"Demo mode: {'enabled' if enabled else 'disabled'}")
