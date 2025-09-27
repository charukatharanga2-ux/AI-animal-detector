"""
Test camera availability and functionality
"""

import cv2
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_cameras():
    """Test available cameras"""
    print("Testing Camera Availability...")
    print("=" * 40)
    
    available_cameras = []
    
    # Test cameras 0-5
    for i in range(6):
        print(f"Testing camera {i}...")
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"  Camera {i}: OK - {frame.shape}")
                available_cameras.append(i)
            else:
                print(f"  Camera {i}: Failed to read frame")
            cap.release()
        else:
            print(f"  Camera {i}: Not available")
    
    print(f"\nAvailable cameras: {available_cameras}")
    
    if available_cameras:
        print(f"\nUsing camera {available_cameras[0]} for testing...")
        cap = cv2.VideoCapture(available_cameras[0])
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Successfully captured frame: {frame.shape}")
                print("Camera is working!")
            else:
                print("Failed to capture frame")
            cap.release()
        else:
            print("Failed to open camera")
    else:
        print("No cameras available!")
        print("Please check:")
        print("1. Camera is connected")
        print("2. Camera drivers are installed")
        print("3. No other applications are using the camera")

if __name__ == "__main__":
    test_cameras()
