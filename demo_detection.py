"""
Demo script to showcase the advanced wildlife detection system
"""

import cv2
import numpy as np
import time
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detection.advanced_wildlife_detector import AdvancedWildlifeDetector
from detection.peacock_detector import PeacockDetector
from detection.human_filter import HumanFilter

def create_demo_frame():
    """Create a demo frame with simulated wildlife"""
    # Create a 640x480 frame
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some background elements
    cv2.rectangle(frame, (0, 0), (640, 480), (34, 139, 34), -1)  # Forest green background
    
    # Add some trees (simple rectangles)
    cv2.rectangle(frame, (50, 200), (80, 400), (101, 67, 33), -1)  # Tree trunk
    cv2.circle(frame, (65, 180), 40, (0, 100, 0), -1)  # Tree top
    
    cv2.rectangle(frame, (500, 150), (530, 350), (101, 67, 33), -1)  # Tree trunk
    cv2.circle(frame, (515, 130), 35, (0, 100, 0), -1)  # Tree top
    
    # Add some grass
    for i in range(0, 640, 20):
        cv2.line(frame, (i, 400), (i+10, 480), (0, 150, 0), 2)
    
    return frame

def demo_detection():
    """Demo the detection system"""
    print("Wildlife Detection System Demo")
    print("=" * 40)
    
    # Initialize detectors
    wildlife_detector = AdvancedWildlifeDetector()
    peacock_detector = PeacockDetector()
    human_filter = HumanFilter()
    
    print("Detectors initialized successfully!")
    
    # Create demo frame
    frame = create_demo_frame()
    
    print("\nRunning detection on demo frame...")
    
    # Run detection
    wildlife_detections = wildlife_detector.detect_animals(frame)
    peacock_detections = peacock_detector.detect_peacocks(frame)
    
    print(f"Wildlife detections: {len(wildlife_detections)}")
    print(f"Peacock detections: {len(peacock_detections)}")
    
    # Combine detections
    all_detections = wildlife_detections + peacock_detections
    
    # Filter out humans
    filtered_detections = human_filter.filter_human_detections(frame, all_detections)
    
    print(f"After human filtering: {len(filtered_detections)} detections")
    
    # Draw detections
    if wildlife_detections:
        frame = wildlife_detector.draw_detections(frame, wildlife_detections)
    
    if peacock_detections:
        frame = peacock_detector.draw_peacock_detection(frame, peacock_detections)
    
    # Display frame
    cv2.imshow("Wildlife Detection Demo", frame)
    print("\nDemo frame displayed! Press any key to close...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("\nDemo completed!")

def demo_accuracy_features():
    """Demo the accuracy features"""
    print("\nAccuracy Features Demo")
    print("=" * 30)
    
    print("1. Human Filter:")
    print("   - Prevents humans from being detected as pigs")
    print("   - Uses YOLOv8 person detection")
    print("   - Filters out overlapping regions")
    
    print("\n2. Peacock Detection:")
    print("   - Specialized color analysis (HSV)")
    print("   - Detects blue, green, teal plumage")
    print("   - Unique crosshair markers")
    print("   - High confidence threshold (70%)")
    
    print("\n3. Advanced Wildlife Detection:")
    print("   - Animal-specific confidence thresholds")
    print("   - Aspect ratio validation")
    print("   - Size-based filtering")
    print("   - Professional visual indicators")
    
    print("\n4. Multi-Detector System:")
    print("   - Wildlife detector for general animals")
    print("   - Peacock detector for birds")
    print("   - Human filter for false positives")
    print("   - Intelligent detection combination")

def main():
    """Run the demo"""
    print("Advanced Wildlife Detection System Demo")
    print("=" * 50)
    
    try:
        demo_detection()
        demo_accuracy_features()
        
        print("\n" + "=" * 50)
        print("Demo completed successfully!")
        print("The system is ready for real wildlife detection!")
        
    except Exception as e:
        print(f"Demo error: {e}")
        print("Please ensure all dependencies are installed")

if __name__ == "__main__":
    main()
