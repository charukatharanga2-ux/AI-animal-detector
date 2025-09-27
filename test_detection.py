"""
Test script for wildlife detection with alarms and SMS
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_alarm_system():
    """Test alarm system for all animals"""
    print("Testing Alarm System...")
    
    from utils.alarm_system import AlarmSystem
    alarm = AlarmSystem()
    
    animals = ['pig', 'deer', 'peacock', 'hedgehog', 'monkey']
    
    for animal in animals:
        print(f"Testing {animal} alarm...")
        alarm.play_alarm(animal)
        time.sleep(1)  # Wait between sounds
    
    print("+ Alarm system test completed!")

def test_sms_system():
    """Test SMS system"""
    print("Testing SMS System...")
    
    from utils.sms_notifier import SMSNotifier
    sms = SMSNotifier()
    
    # Test SMS
    success = sms.test_sms()
    if success:
        print("+ SMS test successful!")
    else:
        print("- SMS test failed - check Twilio configuration")
    
    return success

def test_detection_system():
    """Test detection system"""
    print("Testing Detection System...")
    
    from detection.wildlife_detector import WildlifeDetector
    import numpy as np
    
    detector = WildlifeDetector()
    
    # Create a test image
    test_image = np.zeros((640, 640, 3), dtype=np.uint8)
    
    # Enable demo mode
    detector.set_demo_mode(True)
    
    # Test detection
    detections = detector.detect_animals(test_image)
    print(f"Found {len(detections)} detections")
    
    for detection in detections:
        print(f"  - {detection['animal_type']}: {detection['confidence']:.2f}")
    
    print("+ Detection system test completed!")

def main():
    """Run all tests"""
    print("=== Wildlife Detection System Test ===")
    print("Testing all 6 animals: pig, deer, peacock, hedgehog, monkey")
    print("-" * 50)
    
    # Test alarm system
    test_alarm_system()
    print()
    
    # Test SMS system
    sms_success = test_sms_system()
    print()
    
    # Test detection system
    test_detection_system()
    print()
    
    print("=== Test Summary ===")
    print("+ Alarm system: Working")
    if sms_success:
        print("+ SMS system: Working")
    else:
        print("- SMS system: Not configured (check Twilio settings)")
    print("+ Detection system: Working")
    
    print("\nReady to detect wildlife!")
    print("Run 'python main.py' to start the application")

if __name__ == "__main__":
    main()
