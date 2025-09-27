"""
Test script for the Wildlife Detection Application
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        import config
        print("+ config imported")
    except Exception as e:
        print(f"- config import failed: {e}")
        return False
    
    try:
        from utils.database import DetectionDatabase
        print("+ database imported")
    except Exception as e:
        print(f"- database import failed: {e}")
        return False
    
    try:
        from utils.sms_notifier import SMSNotifier
        print("+ sms_notifier imported")
    except Exception as e:
        print(f"- sms_notifier import failed: {e}")
        return False
    
    try:
        from utils.alarm_system import AlarmSystem
        print("+ alarm_system imported")
    except Exception as e:
        print(f"- alarm_system import failed: {e}")
        return False
    
    try:
        from utils.translator import LanguageTranslator
        print("+ translator imported")
    except Exception as e:
        print(f"- translator import failed: {e}")
        return False
    
    try:
        from detection.yolo_detector import YOLODetector
        print("+ yolo_detector imported")
    except Exception as e:
        print(f"- yolo_detector import failed: {e}")
        return False
    
    try:
        from camera.camera_manager import CameraManager
        print("+ camera_manager imported")
    except Exception as e:
        print(f"- camera_manager import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database functionality"""
    print("\nTesting database...")
    
    try:
        from utils.database import DetectionDatabase
        db = DetectionDatabase("test.db")
        
        # Test adding detection
        db.add_detection("pig", 0.85, [100, 100, 50, 50])
        
        # Test getting detections
        detections = db.get_detections(limit=5)
        print(f"+ Database test passed - found {len(detections)} detections")
        
        # Cleanup
        if os.path.exists("test.db"):
            os.remove("test.db")
        
        return True
    except Exception as e:
        print(f"- Database test failed: {e}")
        return False

def test_alarm_system():
    """Test alarm system"""
    print("\nTesting alarm system...")
    
    try:
        from utils.alarm_system import AlarmSystem
        alarm = AlarmSystem()
        
        # Check if sound files exist
        sound_files = [
            "sounds/pig_alarm.wav",
            "sounds/deer_alarm.wav", 
            "sounds/peacock_alarm.wav",
            "sounds/hedgehog_alarm.wav",
            "sounds/monkey_alarm.wav"
        ]
        
        for sound_file in sound_files:
            if os.path.exists(sound_file):
                print(f"+ {sound_file} exists")
            else:
                print(f"- {sound_file} missing")
                return False
        
        print("+ Alarm system test passed")
        return True
    except Exception as e:
        print(f"- Alarm system test failed: {e}")
        return False

def test_yolo_model():
    """Test YOLO model"""
    print("\nTesting YOLO model...")
    
    try:
        from detection.yolo_detector import YOLODetector
        detector = YOLODetector()
        
        if detector.is_model_loaded():
            print("+ YOLO model loaded successfully")
            return True
        else:
            print("- YOLO model not loaded")
            return False
    except Exception as e:
        print(f"- YOLO model test failed: {e}")
        return False

def test_camera():
    """Test camera functionality"""
    print("\nTesting camera...")
    
    try:
        from camera.camera_manager import CameraManager
        camera_manager = CameraManager()
        
        cameras = camera_manager.get_available_cameras()
        print(f"+ Found {len(cameras)} cameras: {cameras}")
        
        if len(cameras) > 0:
            print("+ Camera test passed")
            return True
        else:
            print("! No cameras found - this is normal if no camera is connected")
            return True
    except Exception as e:
        print(f"- Camera test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Wildlife Detection App Test ===")
    
    tests = [
        test_imports,
        test_database,
        test_alarm_system,
        test_yolo_model,
        test_camera
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("+ All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("python main.py")
    else:
        print("- Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
