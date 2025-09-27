"""
Configuration file for the Wildlife Detection Application
"""

# Animal classes to detect
ANIMAL_CLASSES = {
    0: 'pig',
    1: 'deer', 
    2: 'peacock',
    3: 'hedgehog',
    4: 'monkey'
}

# Alarm sound files (create these in sounds/ directory)
ALARM_SOUNDS = {
    'pig': 'sounds/pig_alarm.wav',
    'deer': 'sounds/deer_alarm.wav',
    'peacock': 'sounds/peacock_alarm.wav',
    'hedgehog': 'sounds/hedgehog_alarm.wav',
    'monkey': 'sounds/monkey_alarm.wav'
}

# SMS Configuration (set your Twilio credentials)
TWILIO_CONFIG = {
    'account_sid': 'YOUR_TWILIO_ACCOUNT_SID',
    'auth_token': 'YOUR_TWILIO_AUTH_TOKEN',
    'from_number': 'YOUR_TWILIO_PHONE_NUMBER',
    'to_number': 'YOUR_PHONE_NUMBER'
}

# Camera settings
CAMERA_SETTINGS = {
    'width': 1920,
    'height': 1080,
    'fps': 30
}

# UI Colors
UI_COLORS = {
    'background': '#FFFFFF',
    'primary': '#4A90E2',
    'secondary': '#F5F5F5',
    'text': '#333333',
    'accent': '#7ED321'
}

# Language support
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German'
}

# YOLOv8 model configuration
MODEL_CONFIG = {
    'model_path': 'models/yolov8n.pt',
    'confidence_threshold': 0.5,
    'iou_threshold': 0.45
}
