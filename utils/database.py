"""
Database utilities for storing detection history
"""

import sqlite3
import json
from datetime import datetime
import os

class DetectionDatabase:
    def __init__(self, db_path="detections.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create detections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp TEXT NOT NULL,
                bbox_x INTEGER,
                bbox_y INTEGER,
                bbox_width INTEGER,
                bbox_height INTEGER,
                image_path TEXT
            )
        ''')
        
        # Create settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_detection(self, animal_type, confidence, bbox, image_path=None):
        """Add a new detection to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO detections 
            (animal_type, confidence, timestamp, bbox_x, bbox_y, bbox_width, bbox_height, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            animal_type,
            confidence,
            datetime.now().isoformat(),
            bbox[0], bbox[1], bbox[2], bbox[3],
            image_path
        ))
        
        conn.commit()
        conn.close()
    
    def get_detections(self, limit=100, animal_type=None):
        """Get detection history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if animal_type:
            cursor.execute('''
                SELECT * FROM detections 
                WHERE animal_type = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (animal_type, limit))
        else:
            cursor.execute('''
                SELECT * FROM detections 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_detection_stats(self):
        """Get detection statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total detections
        cursor.execute('SELECT COUNT(*) FROM detections')
        total_detections = cursor.fetchone()[0]
        
        # Detections by animal type
        cursor.execute('''
            SELECT animal_type, COUNT(*) as count 
            FROM detections 
            GROUP BY animal_type
        ''')
        animal_stats = dict(cursor.fetchall())
        
        # Recent detections (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) FROM detections 
            WHERE datetime(timestamp) > datetime('now', '-1 day')
        ''')
        recent_detections = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_detections': total_detections,
            'animal_stats': animal_stats,
            'recent_detections': recent_detections
        }
    
    def save_setting(self, key, value):
        """Save a setting to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) 
            VALUES (?, ?)
        ''', (key, value))
        
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        """Get a setting from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result[0]
        return default
