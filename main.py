"""
Main Wildlife Detection Application
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import os
import sys
import pygame
from tkinter import font

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import UI_COLORS, ANIMAL_CLASSES
from utils.database import DetectionDatabase
from utils.sms_notifier import SMSNotifier
from utils.alarm_system import AlarmSystem
from utils.translator import LanguageTranslator
from detection.ultra_accurate_detector import UltraAccurateWildlifeDetector
from detection.peacock_detector import PeacockDetector
from detection.human_filter import HumanFilter
from camera.camera_manager import CameraManager

class WildlifeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🦌 Wildlife Detection System - Advanced AI Monitoring")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#1a1a1a', 
            'bg_card': '#2a2a2a',
            'accent': '#00ff88',
            'accent_secondary': '#0088ff',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'danger': '#ff4444',
            'warning': '#ffaa00',
            'success': '#00ff88'
        }
        
        # Configure modern styling
        self.setup_styles()
        
        # Initialize components
        self.database = DetectionDatabase()
        self.sms_notifier = SMSNotifier()
        self.alarm_system = AlarmSystem()
        self.translator = LanguageTranslator()
        self.detector = UltraAccurateWildlifeDetector()
        self.peacock_detector = PeacockDetector()
        self.human_filter = HumanFilter()
        self.camera_manager = CameraManager()
        
        # Detection state
        self.detection_running = False
        self.last_detection_time = {}
        self.detection_count = 0
        self.fps_counter = 0
        self.last_fps_time = time.time()
        
        # Create GUI
        self.create_gui()
        
        # Start camera update loop
        self.update_camera_feed()
    
    def setup_styles(self):
        """Setup modern UI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='black',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent_secondary'])])
        
        # Configure danger button style
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        # Configure card frame style
        style.configure('Card.TFrame',
                       background=self.colors['bg_card'],
                       relief='flat',
                       borderwidth=1)
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 12))
        
        style.configure('Info.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 10, 'bold'))
    
    def create_gui(self):
        """Create the main GUI with modern design"""
        # Create header
        self.create_header()
        
        # Create main content area
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create notebook for tabs with modern styling
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Style the notebook
        style = ttk.Style()
        style.configure('TNotebook', background=self.colors['bg_secondary'])
        style.configure('TNotebook.Tab', 
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent']),
                           ('active', self.colors['bg_card'])])
        
        # Create tabs with modern design
        self.create_live_feed_tab()
        self.create_settings_tab()
        self.create_alarm_test_tab()
        self.create_help_tab()
        self.create_history_tab()
        self.create_statistics_tab()
        
        # Create modern status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create modern header with title and status"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="🦌 Wildlife Detection System",
                              font=('Segoe UI', 20, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'])
        title_label.pack(side='left', padx=20, pady=20)
        
        # Status indicator
        self.status_indicator = tk.Label(header_frame,
                                       text="● READY",
                                       font=('Segoe UI', 12, 'bold'),
                                       bg=self.colors['bg_secondary'],
                                       fg=self.colors['success'])
        self.status_indicator.pack(side='right', padx=20, pady=20)
        
        # Detection counter
        self.detection_counter = tk.Label(header_frame,
                                        text="Detections: 0",
                                        font=('Segoe UI', 10),
                                        bg=self.colors['bg_secondary'],
                                        fg=self.colors['text_secondary'])
        self.detection_counter.pack(side='right', padx=20, pady=20)
    
    def create_live_feed_tab(self):
        """Create modern live camera feed tab"""
        self.live_frame = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(self.live_frame, text="📹 Live Feed")
        
        # Control panel with modern design
        control_card = tk.Frame(self.live_frame, bg=self.colors['bg_card'], relief='flat', bd=1)
        control_card.pack(fill='x', padx=20, pady=10)
        
        # Title
        title_label = tk.Label(control_card, 
                              text="🎯 Wildlife Detection Control",
                              font=('Segoe UI', 14, 'bold'),
                              bg=self.colors['bg_card'],
                              fg=self.colors['text_primary'])
        title_label.pack(pady=15)
        
        # Control buttons frame
        button_frame = tk.Frame(control_card, bg=self.colors['bg_card'])
        button_frame.pack(pady=10)
        
        # Start/Stop buttons with modern styling
        self.start_btn = tk.Button(button_frame, 
                                  text="🚀 START DETECTION",
                                  command=self.start_detection,
                                  bg=self.colors['success'],
                                  fg='black',
                                  font=('Segoe UI', 12, 'bold'),
                                  padx=20, pady=10,
                                  relief='flat',
                                  cursor='hand2')
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(button_frame, 
                                 text="⏹️ STOP DETECTION",
                                 command=self.stop_detection,
                                 bg=self.colors['danger'],
                                 fg='white',
                                 font=('Segoe UI', 12, 'bold'),
                                 padx=20, pady=10,
                                 relief='flat',
                                 state='disabled',
                                 cursor='hand2')
        self.stop_btn.pack(side='left', padx=10)
        
        # Settings frame
        settings_frame = tk.Frame(control_card, bg=self.colors['bg_card'])
        settings_frame.pack(pady=10)
        
        # Camera selection
        tk.Label(settings_frame, 
                text="📷 Camera:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(side='left', padx=5)
        
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(settings_frame, textvariable=self.camera_var,
                                        state='readonly', width=15,
                                        font=('Segoe UI', 10))
        self.camera_combo.pack(side='left', padx=5)
        self.camera_combo.bind('<<ComboboxSelected>>', self.on_camera_change)
        
        # Language selection
        tk.Label(settings_frame, 
                text="🌐 Language:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(side='left', padx=(20, 5))
        
        self.language_var = tk.StringVar(value='en')
        self.language_combo = ttk.Combobox(settings_frame, textvariable=self.language_var,
                                          values=list(self.translator.translations.keys()),
                                          state='readonly', width=10,
                                          font=('Segoe UI', 10))
        self.language_combo.pack(side='left', padx=5)
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Camera feed display with modern frame
        feed_card = tk.Frame(self.live_frame, bg=self.colors['bg_card'], relief='flat', bd=1)
        feed_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Feed title
        feed_title = tk.Label(feed_card,
                             text="📹 Live Camera Feed",
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'])
        feed_title.pack(pady=10)
        
        # Camera display
        self.camera_label = tk.Label(feed_card, 
                                    text="🎥 Camera Feed\n\nClick 'START DETECTION' to begin",
                                    font=('Segoe UI', 14),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_secondary'],
                                    relief='flat')
        self.camera_label.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Detection info with modern styling
        info_card = tk.Frame(self.live_frame, bg=self.colors['bg_card'], relief='flat', bd=1)
        info_card.pack(fill='x', padx=20, pady=10)
        
        info_title = tk.Label(info_card,
                             text="📊 Detection Log",
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['bg_card'],
                             fg=self.colors['text_primary'])
        info_title.pack(pady=10)
        
        self.detection_info = tk.Text(info_card, 
                                     height=6, 
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_primary'],
                                     font=('Consolas', 9),
                                     relief='flat',
                                     bd=0)
        self.detection_info.pack(fill='x', padx=20, pady=(0, 20))
        
        # Update camera list
        self.update_camera_list()
    
    def create_settings_tab(self):
        """Create settings tab"""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text=self.translator.get_text('settings'))
        
        # SMS Settings
        sms_frame = ttk.LabelFrame(self.settings_frame, text="SMS Settings")
        sms_frame.pack(fill='x', padx=10, pady=5)
        
        self.sms_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(sms_frame, text=self.translator.get_text('sms_enabled'),
                       variable=self.sms_enabled_var).pack(anchor='w', padx=5, pady=2)
        
        ttk.Label(sms_frame, text="Phone Number:").pack(anchor='w', padx=5)
        self.phone_entry = ttk.Entry(sms_frame, width=20)
        self.phone_entry.pack(anchor='w', padx=5, pady=2)
        
        # Alarm Settings
        alarm_frame = ttk.LabelFrame(self.settings_frame, text="Alarm Settings")
        alarm_frame.pack(fill='x', padx=10, pady=5)
        
        self.alarm_enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(alarm_frame, text=self.translator.get_text('alarm_enabled'),
                       variable=self.alarm_enabled_var).pack(anchor='w', padx=5, pady=2)
        
        # Detection Settings
        detection_frame = ttk.LabelFrame(self.settings_frame, text="Detection Settings")
        detection_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(detection_frame, text="Confidence Threshold:").pack(anchor='w', padx=5)
        self.confidence_var = tk.DoubleVar(value=0.5)
        self.confidence_scale = ttk.Scale(detection_frame, from_=0.1, to=1.0, 
                                        variable=self.confidence_var, orient='horizontal')
        self.confidence_scale.pack(fill='x', padx=5, pady=2)
        
        # Demo Mode
        self.demo_mode_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(detection_frame, text="Demo Mode (Simulate Animal Detections)",
                       variable=self.demo_mode_var, command=self.toggle_demo_mode).pack(anchor='w', padx=5, pady=2)
        
        # Save button
        ttk.Button(self.settings_frame, text=self.translator.get_text('save_settings'),
                  command=self.save_settings).pack(pady=10)
    
    def create_alarm_test_tab(self):
        """Create alarm test tab"""
        self.alarm_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alarm_frame, text=self.translator.get_text('alarm_test'))
        
        # Test buttons for each animal
        for animal in ANIMAL_CLASSES.values():
            btn = ttk.Button(self.alarm_frame, text=f"Test {animal.title()} Alarm",
                           command=lambda a=animal: self.test_animal_alarm(a))
            btn.pack(pady=5, padx=10, fill='x')
        
        # Test all alarms button
        ttk.Button(self.alarm_frame, text="Test All Alarms",
                  command=self.test_all_alarms).pack(pady=10, padx=10, fill='x')
        
        # Test SMS button
        ttk.Button(self.alarm_frame, text=self.translator.get_text('test_sms'),
                  command=self.test_sms).pack(pady=5, padx=10, fill='x')
    
    def create_help_tab(self):
        """Create help and guidelines tab"""
        self.help_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.help_frame, text=self.translator.get_text('help'))
        
        help_text = """
Wildlife Detection Application Help

1. Live Camera Feed:
   - Click 'Start Detection' to begin animal detection
   - Select camera from dropdown if multiple cameras available
   - Detected animals will be highlighted with bounding boxes

2. Settings:
   - Configure SMS notifications with your phone number
   - Enable/disable alarm sounds
   - Adjust detection confidence threshold

3. Alarm Test:
   - Test alarm sounds for each animal type
   - Test SMS notifications

4. History:
   - View detection history with timestamps
   - See statistics and detection counts

5. Supported Animals:
   - Pigs
   - Deer
   - Peacocks
   - Hedgehogs
   - Monkeys

6. Requirements:
   - Webcam or USB camera
   - Internet connection for SMS
   - Python 3.8+

For support, check the README.md file.
        """
        
        help_label = tk.Text(self.help_frame, wrap='word', height=20)
        help_label.pack(fill='both', expand=True, padx=10, pady=10)
        help_label.insert('1.0', help_text)
        help_label.config(state='disabled')
    
    def create_history_tab(self):
        """Create history tab"""
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text=self.translator.get_text('history'))
        
        # History listbox
        self.history_listbox = tk.Listbox(self.history_frame, height=15)
        self.history_listbox.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Refresh button
        ttk.Button(self.history_frame, text="Refresh History",
                  command=self.refresh_history).pack(pady=5)
        
        # Load initial history
        self.refresh_history()
    
    def create_statistics_tab(self):
        """Create statistics tab"""
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text=self.translator.get_text('statistics'))
        
        # Statistics display
        self.stats_text = tk.Text(self.stats_frame, height=15, width=50)
        self.stats_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Refresh button
        ttk.Button(self.stats_frame, text="Refresh Statistics",
                  command=self.refresh_statistics).pack(pady=5)
        
        # Load initial statistics
        self.refresh_statistics()
    
    def create_status_bar(self):
        """Create modern status bar"""
        self.status_bar = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=40)
        self.status_bar.pack(fill='x', side='bottom')
        self.status_bar.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(self.status_bar, 
                                    text="🟢 System Ready",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['success'])
        self.status_label.pack(side='left', padx=20, pady=10)
        
        # Detection status
        self.detection_status = tk.Label(self.status_bar, 
                                        text="🔴 Detection: Stopped",
                                        font=('Segoe UI', 10, 'bold'),
                                        bg=self.colors['bg_secondary'],
                                        fg=self.colors['danger'])
        self.detection_status.pack(side='right', padx=20, pady=10)
        
        # FPS counter
        self.fps_label = tk.Label(self.status_bar,
                                   text="FPS: --",
                                   font=('Segoe UI', 10),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_secondary'])
        self.fps_label.pack(side='right', padx=20, pady=10)
    
    def update_camera_list(self):
        """Update camera selection dropdown"""
        cameras = self.camera_manager.get_available_cameras()
        self.camera_combo['values'] = [f"Camera {i}" for i in cameras]
        if cameras:
            self.camera_combo.current(0)
            self.camera_manager.set_camera(cameras[0])
    
    def on_camera_change(self, event):
        """Handle camera selection change"""
        selection = self.camera_combo.get()
        if selection:
            camera_index = int(selection.split()[-1])
            self.camera_manager.set_camera(camera_index)
    
    def on_language_change(self, event):
        """Handle language selection change"""
        language = self.language_var.get()
        self.translator.set_language(language)
        # Note: In a full implementation, you would refresh all text labels here
    
    def start_detection(self):
        """Start animal detection"""
        if not self.detector.is_model_loaded():
            messagebox.showerror("Error", "YOLOv8 model not loaded. Please check your internet connection.")
            return
        
        self.detection_running = True
        self.start_btn.config(state='disabled', bg=self.colors['bg_secondary'])
        self.stop_btn.config(state='normal', bg=self.colors['danger'])
        self.detection_status.config(text="🟢 Detection: Running", fg=self.colors['success'])
        self.status_indicator.config(text="● DETECTING", fg=self.colors['warning'])
        
        # Start camera if not running
        if not self.camera_manager.is_camera_running():
            self.camera_manager.start_camera()
    
    def stop_detection(self):
        """Stop animal detection"""
        self.detection_running = False
        self.start_btn.config(state='normal', bg=self.colors['success'])
        self.stop_btn.config(state='disabled', bg=self.colors['bg_secondary'])
        self.detection_status.config(text="🔴 Detection: Stopped", fg=self.colors['danger'])
        self.status_indicator.config(text="● READY", fg=self.colors['success'])
    
    def update_camera_feed(self):
        """Update camera feed display with FPS tracking"""
        current_time = time.time()
        self.fps_counter += 1
        
        # Update FPS every second
        if current_time - self.last_fps_time >= 1.0:
            fps = self.fps_counter / (current_time - self.last_fps_time)
            self.fps_label.config(text=f"FPS: {fps:.1f}")
            self.fps_counter = 0
            self.last_fps_time = current_time
        
        if self.camera_manager.is_camera_running():
            frame = self.camera_manager.get_frame()
            if frame is not None:
                # Run detection if enabled
                detections = []
                if self.detection_running:
                    # Use advanced wildlife detector
                    wildlife_detections = self.detector.detect_animals(frame)
                    
                    # Use specialized peacock detector
                    peacock_detections = self.peacock_detector.detect_peacocks(frame)
                    
                    # Combine detections, prioritizing peacock detector for peacocks
                    detections = wildlife_detections.copy()
                    
                    # Add peacock detections if they're more confident
                    for peacock_det in peacock_detections:
                        # Check if we already have a peacock detection
                        existing_peacock = any(d['animal_type'] == 'peacock' for d in detections)
                        if not existing_peacock or peacock_det['confidence'] > 0.8:
                            detections.append(peacock_det)
                    
                    # Filter out human detections to prevent false positives
                    detections = self.human_filter.filter_human_detections(frame, detections)
                    
                    self.handle_detections(detections)
                
                # Draw detections on frame
                if detections:
                    # Separate peacock detections for special drawing
                    peacock_detections = [d for d in detections if d['animal_type'] == 'peacock']
                    other_detections = [d for d in detections if d['animal_type'] != 'peacock']
                    
                    # Draw other animals
                    if other_detections:
                        frame = self.detector.draw_detections(frame, other_detections)
                    
                    # Draw peacocks with specialized markers
                    if peacock_detections:
                        frame = self.peacock_detector.draw_peacock_detection(frame, peacock_detections)
                
                # Convert frame for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                
                # Resize for display
                display_width = 800
                display_height = 600
                frame_pil = frame_pil.resize((display_width, display_height), Image.Resampling.LANCZOS)
                
                frame_tk = ImageTk.PhotoImage(frame_pil)
                self.camera_label.config(image=frame_tk, text="")
                self.camera_label.image = frame_tk
        else:
            # Show placeholder when no camera
            self.camera_label.config(image="", 
                                   text="🎥 Camera Feed\n\nClick 'START DETECTION' to begin",
                                   font=('Segoe UI', 14),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_secondary'])
        
        # Schedule next update
        self.root.after(33, self.update_camera_feed)  # ~30 FPS
    
    def handle_detections(self, detections):
        """Handle detected animals"""
        current_time = time.time()
        
        for detection in detections:
            animal_type = detection['animal_type']
            confidence = detection['confidence']
            
            # Check if enough time has passed since last detection of this animal
            if animal_type in self.last_detection_time:
                if current_time - self.last_detection_time[animal_type] < 5:  # 5 second cooldown
                    continue
            
            # Update last detection time
            self.last_detection_time[animal_type] = current_time
            
            # Update detection counter
            self.detection_count += 1
            self.detection_counter.config(text=f"Detections: {self.detection_count}")
            
            # Log detection
            self.log_detection(animal_type, confidence, detection['bbox'])
            
            # Play alarm immediately
            print(f"🚨 ALARM: {animal_type.upper()} detected with {confidence:.2f} confidence!")
            if self.alarm_enabled_var.get():
                self.alarm_system.play_alarm(animal_type)
                print(f"🔊 Playing {animal_type} alarm sound")
            
            # Send SMS immediately
            if self.sms_enabled_var.get():
                print(f"📱 Sending SMS for {animal_type} detection")
                success = self.sms_notifier.send_detection_alert(animal_type, confidence)
                if success:
                    print(f"✅ SMS sent successfully for {animal_type}")
                else:
                    print(f"❌ SMS failed for {animal_type}")
            else:
                print("📱 SMS notifications disabled")
    
    def log_detection(self, animal_type, confidence, bbox):
        """Log detection to database and display"""
        # Save to database
        self.database.add_detection(animal_type, confidence, bbox)
        
        # Update detection info display
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_text = f"{timestamp} - {animal_type.title()} detected (confidence: {confidence:.2f})\n"
        
        self.detection_info.insert('1.0', info_text)
        
        # Keep only last 10 detections in display
        lines = self.detection_info.get('1.0', 'end').split('\n')
        if len(lines) > 11:
            self.detection_info.delete('10.0', 'end')
    
    def test_animal_alarm(self, animal_type):
        """Test alarm for specific animal"""
        self.alarm_system.test_alarm(animal_type)
    
    def test_all_alarms(self):
        """Test all alarm sounds"""
        self.alarm_system.test_all_alarms()
    
    def test_sms(self):
        """Test SMS functionality"""
        if self.sms_notifier.test_sms():
            messagebox.showinfo("Success", "SMS test sent successfully!")
        else:
            messagebox.showerror("Error", "SMS test failed. Check your Twilio configuration.")
    
    def toggle_demo_mode(self):
        """Toggle demo mode for testing"""
        demo_enabled = self.demo_mode_var.get()
        self.detector.set_demo_mode(demo_enabled)
        print(f"Demo mode: {'enabled' if demo_enabled else 'disabled'}")
    
    def save_settings(self):
        """Save application settings"""
        # Save settings to database
        self.database.save_setting('sms_enabled', str(self.sms_enabled_var.get()))
        self.database.save_setting('alarm_enabled', str(self.alarm_enabled_var.get()))
        self.database.save_setting('confidence_threshold', str(self.confidence_var.get()))
        self.database.save_setting('phone_number', self.phone_entry.get())
        self.database.save_setting('demo_mode', str(self.demo_mode_var.get()))
        
        messagebox.showinfo("Success", "Settings saved successfully!")
    
    def refresh_history(self):
        """Refresh detection history"""
        self.history_listbox.delete(0, 'end')
        detections = self.database.get_detections(limit=50)
        
        for detection in detections:
            timestamp = detection[3]
            animal_type = detection[1]
            confidence = detection[2]
            history_text = f"{timestamp} - {animal_type.title()} ({confidence:.2f})"
            self.history_listbox.insert('end', history_text)
    
    def refresh_statistics(self):
        """Refresh statistics display"""
        stats = self.database.get_detection_stats()
        
        stats_text = f"""
Detection Statistics:

Total Detections: {stats['total_detections']}
Recent Detections (24h): {stats['recent_detections']}

Detections by Animal:
"""
        
        for animal, count in stats['animal_stats'].items():
            stats_text += f"{animal.title()}: {count}\n"
        
        self.stats_text.delete('1.0', 'end')
        self.stats_text.insert('1.0', stats_text)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = WildlifeDetectionApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application interrupted by user")
    finally:
        # Cleanup
        if app.camera_manager:
            app.camera_manager.stop_camera()

if __name__ == "__main__":
    main()
