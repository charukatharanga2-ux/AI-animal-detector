"""
Specialized Peacock Detection System
"""

import cv2
import numpy as np
from ultralytics import YOLO
import config

class PeacockDetector:
    def __init__(self):
        self.model = None
        self.load_model()
        
        # Peacock-specific detection parameters
        self.peacock_features = {
            'min_confidence': 0.6,
            'aspect_ratio_range': (0.3, 1.2),  # Tall and narrow
            'min_area_ratio': 0.01,  # At least 1% of frame
            'color_threshold': 100,  # For colorful plumage detection
        }
    
    def load_model(self):
        """Load YOLOv8 model"""
        try:
            self.model = YOLO('yolov8n.pt')
            print("Peacock detection model loaded successfully")
        except Exception as e:
            print(f"Error loading peacock detection model: {e}")
            self.model = None
    
    def detect_peacocks(self, frame):
        """Detect peacocks with specialized filtering"""
        if self.model is None:
            return []
        
        detections = []
        
        try:
            # Run detection specifically for birds (class 14)
            results = self.model(frame, conf=self.peacock_features['min_confidence'])
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        # Only process bird detections (class 14)
                        if class_id == 14:
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            
                            # Apply peacock-specific validation
                            if self._is_peacock_detection(frame, x1, y1, x2, y2, confidence):
                                detections.append({
                                    'animal_type': 'peacock',
                                    'confidence': confidence,
                                    'bbox': [int(x1), int(y1), int(x2-x1), int(y2-y1)],
                                    'class_id': class_id
                                })
                                print(f"🦚 Peacock detected with confidence: {confidence:.2f}")
            
            return detections
            
        except Exception as e:
            print(f"Peacock detection error: {e}")
            return []
    
    def _is_peacock_detection(self, frame, x1, y1, x2, y2, confidence):
        """Validate if detection is likely a peacock"""
        
        # Basic size and aspect ratio checks
        width = x2 - x1
        height = y2 - y1
        aspect_ratio = width / height
        bbox_area = width * height
        frame_area = frame.shape[0] * frame.shape[1]
        
        # Check aspect ratio (peacocks are typically tall)
        if not (self.peacock_features['aspect_ratio_range'][0] < aspect_ratio < self.peacock_features['aspect_ratio_range'][1]):
            return False
        
        # Check minimum area
        if bbox_area < frame_area * self.peacock_features['min_area_ratio']:
            return False
        
        # Extract region of interest
        roi = frame[int(y1):int(y2), int(x1):int(x2)]
        if roi.size == 0:
            return False
        
        # Check for colorful plumage (peacocks have distinctive colors)
        if self._has_peacock_colors(roi):
            return True
        
        # If no specific peacock colors detected, use confidence threshold
        return confidence > 0.7
    
    def _has_peacock_colors(self, roi):
        """Check if region has peacock-like colors"""
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            # Define peacock color ranges (blues, greens, teals)
            peacock_colors = [
                # Blue range
                (np.array([100, 50, 50]), np.array([130, 255, 255])),
                # Green range
                (np.array([40, 50, 50]), np.array([80, 255, 255])),
                # Teal range
                (np.array([80, 50, 50]), np.array([100, 255, 255])),
            ]
            
            total_pixels = roi.shape[0] * roi.shape[1]
            colorful_pixels = 0
            
            for lower, upper in peacock_colors:
                mask = cv2.inRange(hsv, lower, upper)
                colorful_pixels += cv2.countNonZero(mask)
            
            # If more than 10% of pixels are peacock colors, likely a peacock
            color_ratio = colorful_pixels / total_pixels
            return color_ratio > 0.1
            
        except Exception as e:
            print(f"Color analysis error: {e}")
            return False
    
    def draw_peacock_detection(self, frame, detections):
        """Draw specialized peacock detection markers"""
        for detection in detections:
            x, y, w, h = detection['bbox']
            confidence = detection['confidence']
            
            # Peacock-specific color (bright blue-green)
            color = (255, 100, 0)  # Orange for visibility
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 4)
            
            # Draw peacock-specific markers
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Draw crosshair at center
            cv2.line(frame, (center_x - 10, center_y), (center_x + 10, center_y), color, 3)
            cv2.line(frame, (center_x, center_y - 10), (center_x, center_y + 10), color, 3)
            
            # Draw label
            label = f"🦚 PEACOCK: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
            
            # Background
            cv2.rectangle(frame, (x, y - label_size[1] - 15), 
                         (x + label_size[0] + 10, y), color, -1)
            
            # Text
            cv2.putText(frame, label, (x + 5, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        return frame
