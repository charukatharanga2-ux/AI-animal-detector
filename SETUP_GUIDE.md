# Wildlife Detection Application - Setup Guide

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Model and Sounds**
   ```bash
   python setup_model.py
   python create_sounds.py
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```
   or
   ```bash
   python run_app.py
   ```

## 📋 Features Implemented

### ✅ Core Features
- **Real-time Animal Detection**: Using YOLOv8 for detecting pigs, deer, peacocks, hedgehogs, and monkeys
- **Live Camera Feed**: 1080p/30fps camera support with multiple camera switching
- **Alarm System**: Unique alarm sounds for each animal type
- **SMS Notifications**: Twilio integration for instant alerts
- **Detection History**: SQLite database logging with timestamps
- **Multi-language Support**: English and Spanish with Google Translate
- **Modern GUI**: Clean Tkinter interface with tabbed layout

### 🎯 Application Tabs
1. **Live Camera Feed**: Real-time detection with bounding boxes
2. **Settings**: Configure SMS, alarms, and detection parameters
3. **Alarm Test**: Test individual and all alarm sounds
4. **Help & Guidelines**: User documentation and instructions
5. **History**: View detection logs with timestamps
6. **Statistics**: Detection counts and analytics

## 🔧 Configuration

### SMS Setup (Optional)
1. Create a Twilio account at https://twilio.com
2. Get your Account SID, Auth Token, and Phone Number
3. Update `config.py` with your Twilio credentials:
   ```python
   TWILIO_CONFIG = {
       'account_sid': 'YOUR_TWILIO_ACCOUNT_SID',
       'auth_token': 'YOUR_TWILIO_AUTH_TOKEN',
       'from_number': 'YOUR_TWILIO_PHONE_NUMBER',
       'to_number': 'YOUR_PHONE_NUMBER'
   }
   ```

### Camera Setup
- Connect a USB camera or use built-in webcam
- The app will automatically detect available cameras
- Supports multiple camera switching

## 🎵 Alarm Sounds
- **Pig**: Low frequency (400Hz) - 1.5 seconds
- **Deer**: Medium frequency (600Hz) - 1.0 seconds  
- **Peacock**: High frequency (800Hz) - 2.0 seconds
- **Hedgehog**: Low frequency (300Hz) - 0.8 seconds
- **Monkey**: High frequency (700Hz) - 1.2 seconds

## 🗄️ Database
- SQLite database (`detections.db`) stores all detection history
- Includes animal type, confidence, timestamp, and bounding box coordinates
- Automatic cleanup and statistics generation

## 🌐 Language Support
- **English**: Default language
- **Spanish**: Full translation support
- **French/German**: Basic framework (expandable)

## 📊 Detection System
- **YOLOv8 Model**: Pre-trained on COCO dataset
- **Confidence Threshold**: Adjustable (default: 0.5)
- **Real-time Processing**: ~30 FPS on modern hardware
- **Bounding Boxes**: Green rectangles with animal labels

## 🛠️ Troubleshooting

### Common Issues
1. **No Camera Detected**: 
   - Check camera connections
   - Try different camera indices
   - Restart the application

2. **Model Loading Failed**:
   - Check internet connection
   - Run `python setup_model.py` again
   - Verify YOLOv8 installation

3. **SMS Not Working**:
   - Verify Twilio credentials
   - Check phone number format (+1234567890)
   - Test SMS in Alarm Test tab

4. **Sound Issues**:
   - Check if sound files exist in `sounds/` directory
   - Run `python create_sounds.py` to regenerate
   - Verify audio system is working

### Performance Tips
- Use a dedicated GPU for faster detection
- Close other applications for better performance
- Adjust confidence threshold for fewer false positives
- Use lower resolution for faster processing

## 📁 Project Structure
```
AI-farmgard/
├── main.py                 # Main application
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── setup_model.py        # Model setup script
├── create_sounds.py      # Sound file generator
├── test_app.py          # Test suite
├── run_app.py           # Startup script
├── utils/               # Utility modules
│   ├── database.py      # Database operations
│   ├── sms_notifier.py  # SMS notifications
│   ├── alarm_system.py  # Alarm management
│   └── translator.py    # Language translation
├── detection/           # Detection modules
│   └── yolo_detector.py # YOLOv8 integration
├── camera/              # Camera management
│   └── camera_manager.py
├── sounds/              # Alarm sound files
├── models/              # YOLOv8 model files
└── README.md            # Project documentation
```

## 🎯 Usage Instructions

1. **Start Detection**:
   - Click "Start Detection" button
   - Point camera at area to monitor
   - Animals will be highlighted with green boxes

2. **Configure Settings**:
   - Go to Settings tab
   - Enable/disable SMS and alarms
   - Adjust confidence threshold
   - Save settings

3. **Test Alarms**:
   - Go to Alarm Test tab
   - Click individual animal buttons
   - Test SMS notifications

4. **View History**:
   - Check History tab for past detections
   - View Statistics for analytics
   - Export data if needed

## 🔮 Future Enhancements
- Custom wildlife model training
- Mobile app integration
- Cloud storage for detections
- Advanced analytics dashboard
- Multi-camera support
- Email notifications
- Web dashboard

## 📞 Support
- Check the Help tab in the application
- Review this setup guide
- Test individual components with `python test_app.py`
- Check console output for error messages

---

**Ready to detect wildlife! 🦌🐷🦚🦔🐒**
