"""
Language translation utilities
"""

try:
    from googletrans import Translator
except ImportError:
    # Fallback if googletrans is not available
    class Translator:
        def translate(self, text, dest):
            class Result:
                def __init__(self, text):
                    self.text = text
            return Result(text)

import config

class LanguageTranslator:
    def __init__(self):
        self.translator = Translator()
        self.current_language = 'en'
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translation dictionary"""
        self.translations = {
            'en': {
                'app_title': 'Wildlife Detection App',
                'live_feed': 'Live Camera Feed',
                'settings': 'Settings',
                'alarm_test': 'Alarm Test',
                'help': 'Help & Guidelines',
                'history': 'History',
                'statistics': 'Statistics',
                'detected_animals': 'Detected Animals',
                'confidence': 'Confidence',
                'timestamp': 'Timestamp',
                'animal_type': 'Animal Type',
                'start_detection': 'Start Detection',
                'stop_detection': 'Stop Detection',
                'camera_selection': 'Camera Selection',
                'sms_enabled': 'SMS Notifications',
                'alarm_enabled': 'Alarm Sounds',
                'language': 'Language',
                'save_settings': 'Save Settings',
                'test_sms': 'Test SMS',
                'test_alarm': 'Test Alarm',
                'total_detections': 'Total Detections',
                'recent_detections': 'Recent Detections (24h)',
                'detection_history': 'Detection History',
                'no_detections': 'No detections found',
                'pig': 'Pig',
                'deer': 'Deer',
                'peacock': 'Peacock',
                'hedgehog': 'Hedgehog',
                'monkey': 'Monkey'
            },
            'es': {
                'app_title': 'Aplicación de Detección de Vida Silvestre',
                'live_feed': 'Transmisión en Vivo',
                'settings': 'Configuración',
                'alarm_test': 'Prueba de Alarma',
                'help': 'Ayuda y Guías',
                'history': 'Historial',
                'statistics': 'Estadísticas',
                'detected_animals': 'Animales Detectados',
                'confidence': 'Confianza',
                'timestamp': 'Marca de Tiempo',
                'animal_type': 'Tipo de Animal',
                'start_detection': 'Iniciar Detección',
                'stop_detection': 'Detener Detección',
                'camera_selection': 'Selección de Cámara',
                'sms_enabled': 'Notificaciones SMS',
                'alarm_enabled': 'Sonidos de Alarma',
                'language': 'Idioma',
                'save_settings': 'Guardar Configuración',
                'test_sms': 'Probar SMS',
                'test_alarm': 'Probar Alarma',
                'total_detections': 'Detecciones Totales',
                'recent_detections': 'Detecciones Recientes (24h)',
                'detection_history': 'Historial de Detecciones',
                'no_detections': 'No se encontraron detecciones',
                'pig': 'Cerdo',
                'deer': 'Ciervo',
                'peacock': 'Pavo Real',
                'hedgehog': 'Erizo',
                'monkey': 'Mono'
            }
        }
    
    def translate_text(self, text, target_language=None):
        """Translate text to target language"""
        if target_language is None:
            target_language = self.current_language
        
        if target_language == 'en':
            return text
        
        try:
            # Use pre-defined translations first
            if target_language in self.translations:
                if text in self.translations[target_language]:
                    return self.translations[target_language][text]
            
            # Use Google Translate for dynamic translations
            result = self.translator.translate(text, dest=target_language)
            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def set_language(self, language):
        """Set current language"""
        if language in config.LANGUAGES:
            self.current_language = language
    
    def get_text(self, key):
        """Get translated text for a key"""
        if self.current_language in self.translations:
            return self.translations[self.current_language].get(key, key)
        return key
