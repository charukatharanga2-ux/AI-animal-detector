"""
SMS notification utilities using Twilio
"""

from twilio.rest import Client
import config

class SMSNotifier:
    def __init__(self):
        self.client = None
        self.setup_client()
    
    def setup_client(self):
        """Initialize Twilio client"""
        try:
            self.client = Client(
                config.TWILIO_CONFIG['account_sid'],
                config.TWILIO_CONFIG['auth_token']
            )
        except Exception as e:
            print(f"SMS setup failed: {e}")
            self.client = None
    
    def send_detection_alert(self, animal_type, confidence):
        """Send SMS alert for animal detection"""
        if not self.client:
            print("SMS client not configured")
            return False
        
        try:
            message = f"🚨 Wildlife Alert! {animal_type.title()} detected with {confidence:.2f} confidence"
            
            self.client.messages.create(
                body=message,
                from_=config.TWILIO_CONFIG['from_number'],
                to=config.TWILIO_CONFIG['to_number']
            )
            print(f"SMS sent: {animal_type} detection")
            return True
        except Exception as e:
            print(f"SMS sending failed: {e}")
            return False
    
    def test_sms(self):
        """Test SMS functionality"""
        if not self.client:
            return False
        
        try:
            message = "Test message from Wildlife Detection App"
            self.client.messages.create(
                body=message,
                from_=config.TWILIO_CONFIG['from_number'],
                to=config.TWILIO_CONFIG['to_number']
            )
            return True
        except Exception as e:
            print(f"SMS test failed: {e}")
            return False
