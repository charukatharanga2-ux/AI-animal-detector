"""
Camera management for wildlife detection
"""

import cv2
import threading
import time
from config import CAMERA_SETTINGS

class CameraManager:
    def __init__(self):
        self.camera = None
        self.current_camera_index = 0
        self.is_running = False
        self.frame = None
        self.capture_thread = None
        self.available_cameras = []
        self.scan_cameras()
    
    def scan_cameras(self):
        """Scan for available cameras"""
        self.available_cameras = []
        
        # Test cameras 0-9
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    self.available_cameras.append(i)
                cap.release()
        
        print(f"Found {len(self.available_cameras)} cameras: {self.available_cameras}")
    
    def get_available_cameras(self):
        """Get list of available cameras"""
        return self.available_cameras
    
    def set_camera(self, camera_index):
        """Set current camera"""
        if camera_index in self.available_cameras:
            self.current_camera_index = camera_index
            if self.is_running:
                self.stop_camera()
                self.start_camera()
            return True
        return False
    
    def start_camera(self):
        """Start camera capture"""
        if self.is_running:
            return
        
        try:
            self.camera = cv2.VideoCapture(self.current_camera_index)
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_SETTINGS['width'])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_SETTINGS['height'])
            self.camera.set(cv2.CAP_PROP_FPS, CAMERA_SETTINGS['fps'])
            
            if not self.camera.isOpened():
                print(f"Failed to open camera {self.current_camera_index}")
                return False
            
            self.is_running = True
            self.capture_thread = threading.Thread(target=self._capture_frames, daemon=True)
            self.capture_thread.start()
            
            print(f"Camera {self.current_camera_index} started")
            return True
            
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
    
    def stop_camera(self):
        """Stop camera capture"""
        self.is_running = False
        
        if self.capture_thread:
            self.capture_thread.join()
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        print("Camera stopped")
    
    def _capture_frames(self):
        """Capture frames in separate thread"""
        while self.is_running:
            if self.camera and self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    self.frame = frame
                else:
                    print("Failed to read frame")
                    time.sleep(0.1)
            else:
                time.sleep(0.1)
    
    def get_frame(self):
        """Get current frame"""
        return self.frame
    
    def is_camera_running(self):
        """Check if camera is running"""
        return self.is_running and self.camera is not None
    
    def get_camera_info(self):
        """Get current camera information"""
        if self.camera and self.camera.isOpened():
            width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.camera.get(cv2.CAP_PROP_FPS))
            
            return {
                'width': width,
                'height': height,
                'fps': fps,
                'camera_index': self.current_camera_index
            }
        return None
