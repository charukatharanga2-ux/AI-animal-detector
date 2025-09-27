"""
Simple startup script for the Wildlife Detection Application
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the Wildlife Detection Application"""
    print("Starting Wildlife Detection Application...")
    print("Make sure you have a camera connected for the best experience.")
    print("Press Ctrl+C to exit the application.")
    print("-" * 50)
    
    try:
        from main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Please check that all dependencies are installed:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
