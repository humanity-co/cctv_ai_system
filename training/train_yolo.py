import os
from ultralytics import YOLO

def train_cctv_model(data_yaml="cctv_dataset.yaml", epochs=50, imgsz=640, model_type="yolov8n.pt"):
    """
    Fine-tunes a YOLOv8 model for CCTV-specific environments.
    
    Args:
        data_yaml (str): Path to the dataset configuration file.
        epochs (int): Number of training epochs.
        imgsz (int): Image size for training.
        model_type (str): Base model to start from (n, s, m, l, x).
    """
    print(f"🚀 Starting Fine-tuning on {data_yaml}...")
    
    # Load a pre-trained model
    model = YOLO(model_type)
    
    # Train the model
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=16,
        device=0, # Use 'cpu' if no GPU
        name="cctv_finetuned",
        augment=True, # Enable data augmentation for robust CCTV detection
    )
    
    print("✅ Training complete. Model saved in 'runs/detect/cctv_finetuned'")
    return results

if __name__ == "__main__":
    # Example usage (requires a cctv_dataset.yaml and images)
    # train_cctv_model()
    
    # Documentation for the user
    print("""
    --- YOLOv8 CCTV FINE-TUNING GUIDE ---
    1. Organize your Indian CCTV dataset:
       /datasets/cctv/
          /images/train/
          /labels/train/
          /images/val/
          /labels/val/
    2. Create a 'cctv_dataset.yaml':
       path: /Users/devsmac/.gemini/antigravity/scratch/cctv-ai-system/datasets/cctv
       train: images/train
       val: images/val
       names:
         0: person
         1: car
         2: rickshaw
         3: motorbike
         4: license_plate
    3. Run this script to start fine-tuning.
    """)
