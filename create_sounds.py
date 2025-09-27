"""
Create placeholder alarm sound files for the wildlife detection app
"""

import os
import numpy as np
import wave

def create_beep_sound(frequency, duration, filename):
    """Create a simple beep sound file"""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Add some variation to make it more interesting
    wave_data += 0.1 * np.sin(2 * np.pi * frequency * 2 * t)
    
    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Save as WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

def main():
    """Create all alarm sound files"""
    os.makedirs("sounds", exist_ok=True)
    
    # Create different alarm sounds for each animal
    sounds = {
        'pig_alarm.wav': (400, 1.5),      # Lower frequency, longer
        'deer_alarm.wav': (600, 1.0),     # Medium frequency
        'peacock_alarm.wav': (800, 2.0),  # Higher frequency, longer
        'hedgehog_alarm.wav': (300, 0.8),  # Low frequency, short
        'monkey_alarm.wav': (700, 1.2)    # High frequency, medium length
    }
    
    print("Creating alarm sound files...")
    
    for filename, (frequency, duration) in sounds.items():
        filepath = os.path.join("sounds", filename)
        create_beep_sound(frequency, duration, filepath)
        print(f"Created {filepath}")
    
    print("✅ All alarm sound files created successfully!")

if __name__ == "__main__":
    main()
