"""
Setup script to download and configure YOLOv8 model for wildlife detection
"""

import os
import sys
from ultralytics import YOLO
import requests
import zipfile
from pathlib import Path

def download_roboflow_dataset():
    """Download a wildlife detection dataset from Roboflow"""
    print("Setting up wildlife detection model...")
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Download YOLOv8 model (this will auto-download if not present)
    print("Downloading YOLOv8 model...")
    model = YOLO('yolov8n.pt')  # Nano version for faster inference
    
    # Save the model
    model_path = "models/yolov8n.pt"
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Create a custom dataset configuration for wildlife detection
    dataset_config = """
# Wildlife Detection Dataset Configuration
# This configuration maps COCO classes to our target animals

# COCO class mappings for wildlife detection:
# 0: person -> not used
# 1: bicycle -> not used  
# 2: car -> not used
# 3: motorcycle -> not used
# 4: airplane -> not used
# 5: bus -> not used
# 6: train -> not used
# 7: truck -> not used
# 8: boat -> not used
# 9: traffic light -> not used
# 10: fire hydrant -> not used
# 11: stop sign -> not used
# 12: parking meter -> not used
# 13: bench -> not used
# 14: bird -> peacock (closest match)
# 15: cat -> not used
# 16: dog -> not used
# 17: horse -> not used
# 18: sheep -> not used
# 19: cow -> not used
# 20: elephant -> not used
# 21: bear -> not used
# 22: zebra -> not used
# 23: giraffe -> not used
# 24: backpack -> not used
# 25: umbrella -> not used
# 26: handbag -> not used
# 27: tie -> not used
# 28: suitcase -> not used
# 29: frisbee -> not used
# 30: skis -> not used
# 31: snowboard -> not used
# 32: sports ball -> not used
# 33: kite -> not used
# 34: baseball bat -> not used
# 35: baseball glove -> not used
# 36: skateboard -> not used
# 37: surfboard -> not used
# 38: tennis racket -> not used
# 39: bottle -> not used
# 40: wine glass -> not used
# 41: cup -> not used
# 42: fork -> not used
# 43: knife -> not used
# 44: spoon -> not used
# 45: bowl -> not used
# 46: banana -> not used
# 47: apple -> not used
# 48: sandwich -> not used
# 49: orange -> not used
# 50: broccoli -> not used
# 51: carrot -> not used
# 52: hot dog -> not used
# 53: pizza -> not used
# 54: donut -> not used
# 55: cake -> not used
# 56: chair -> not used
# 57: couch -> not used
# 58: potted plant -> not used
# 59: bed -> not used
# 60: dining table -> not used
# 61: toilet -> not used
# 62: tv -> not used
# 63: laptop -> not used
# 64: mouse -> not used
# 65: remote -> not used
# 66: keyboard -> not used
# 67: cell phone -> not used
# 68: microwave -> not used
# 69: oven -> not used
# 70: toaster -> not used
# 71: sink -> not used
# 72: refrigerator -> not used
# 73: book -> not used
# 74: clock -> not used
# 75: vase -> not used
# 76: scissors -> not used
# 77: teddy bear -> not used
# 78: hair drier -> not used
# 79: toothbrush -> not used

# For wildlife detection, we'll use:
# - COCO class 14 (bird) for peacock detection
# - We'll need to train a custom model for pigs, deer, hedgehogs, monkeys
# - For now, we'll use the base model and filter results
"""
    
    with open("models/dataset_config.txt", "w") as f:
        f.write(dataset_config)
    
    print("Dataset configuration created")
    return model_path

def create_custom_classes():
    """Create custom class mapping for wildlife detection"""
    # Since we need specific animals not in COCO, we'll create a mapping
    # that uses the closest COCO classes and filters for our target animals
    
    custom_classes = {
        # COCO class 14 (bird) -> peacock
        14: 'peacock',
        # We'll need to add custom detection for other animals
        # For now, we'll use a simple approach
    }
    
    return custom_classes

def test_model():
    """Test the downloaded model"""
    print("Testing model...")
    
    try:
        model = YOLO('models/yolov8n.pt')
        print("Model loaded successfully!")
        
        # Test with a simple image
        import numpy as np
        test_image = np.zeros((640, 640, 3), dtype=np.uint8)
        results = model(test_image)
        print("Model inference test passed!")
        
        return True
    except Exception as e:
        print(f"Model test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=== Wildlife Detection Model Setup ===")
    
    # Download and setup model
    model_path = download_roboflow_dataset()
    
    # Create custom classes
    custom_classes = create_custom_classes()
    
    # Test model
    if test_model():
        print("✅ Model setup completed successfully!")
        print(f"Model location: {model_path}")
        print("\nNote: The base YOLOv8 model will detect general objects.")
        print("For specific wildlife detection, you may need to:")
        print("1. Train a custom model with wildlife data")
        print("2. Use a pre-trained wildlife detection model")
        print("3. Filter COCO results for relevant animals")
    else:
        print("❌ Model setup failed!")
        return False
    
    return True

if __name__ == "__main__":
    main()
