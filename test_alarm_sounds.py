"""
Test alarm sounds for all animals
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all_alarm_sounds():
    """Test alarm sounds for all 6 animals"""
    print("Testing Wildlife Alarm Sounds...")
    print("=" * 40)
    
    from utils.alarm_system import AlarmSystem
    alarm = AlarmSystem()
    
    animals = ['pig', 'deer', 'peacock', 'hedgehog', 'monkey']
    
    for i, animal in enumerate(animals, 1):
        print(f"{i}. Testing {animal.upper()} alarm...")
        alarm.play_alarm(animal)
        time.sleep(2)  # Wait between sounds to hear each one
    
    print("\nAll alarm sounds tested!")
    print("If you heard 5 different sounds, the alarm system is working!")

if __name__ == "__main__":
    test_all_alarm_sounds()
