"""
Alarm system for animal detection alerts
"""

import os
import threading
import config
import sys

# Try different audio libraries for better Windows compatibility
try:
    import pygame
    pygame.mixer.init()
    AUDIO_LIB = 'pygame'
except ImportError:
    try:
        from playsound import playsound
        AUDIO_LIB = 'playsound'
    except ImportError:
        try:
            import winsound
            AUDIO_LIB = 'winsound'
        except ImportError:
            AUDIO_LIB = None

class AlarmSystem:
    def __init__(self):
        self.sound_files = config.ALARM_SOUNDS
        self.create_sound_files()
    
    def create_sound_files(self):
        """Create placeholder sound files if they don't exist"""
        os.makedirs("sounds", exist_ok=True)
        
        for animal, sound_path in self.sound_files.items():
            if not os.path.exists(sound_path):
                # Create a simple beep sound file (placeholder)
                self.create_beep_sound(sound_path)
    
    def create_beep_sound(self, file_path):
        """Create a simple beep sound file"""
        try:
            import numpy as np
            import wave
            
            # Generate a simple beep sound
            sample_rate = 44100
            duration = 1.0  # seconds
            frequency = 800  # Hz
            
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            wave_data = np.sin(2 * np.pi * frequency * t) * 0.3
            
            # Convert to 16-bit integers
            wave_data = (wave_data * 32767).astype(np.int16)
            
            # Save as WAV file
            with wave.open(file_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(wave_data.tobytes())
                
        except ImportError:
            # If numpy is not available, create an empty file
            with open(file_path, 'w') as f:
                f.write("")
    
    def play_alarm(self, animal_type):
        """Play alarm sound for detected animal"""
        if animal_type in self.sound_files:
            sound_path = self.sound_files[animal_type]
            if os.path.exists(sound_path):
                # Play sound in a separate thread to avoid blocking
                threading.Thread(
                    target=self._play_sound,
                    args=(sound_path,),
                    daemon=True
                ).start()
    
    def _play_sound(self, sound_path):
        """Play sound file using available audio library"""
        try:
            if AUDIO_LIB == 'pygame':
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
                # Wait for sound to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
            elif AUDIO_LIB == 'playsound':
                playsound(sound_path)
            elif AUDIO_LIB == 'winsound':
                # Use Windows system beep as fallback
                winsound.Beep(800, 1000)  # 800Hz for 1 second
            else:
                print(f"No audio library available for {sound_path}")
        except Exception as e:
            print(f"Error playing sound {sound_path}: {e}")
            # Fallback to system beep
            try:
                import winsound
                winsound.Beep(800, 1000)
            except:
                print("No audio available")
    
    def test_alarm(self, animal_type):
        """Test alarm for specific animal"""
        self.play_alarm(animal_type)
    
    def test_all_alarms(self):
        """Test all alarm sounds"""
        for animal_type in self.sound_files.keys():
            print(f"Testing alarm for {animal_type}")
            self.play_alarm(animal_type)
            import time
            time.sleep(1)  # Wait between sounds
