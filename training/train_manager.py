import os
import argparse
from ultralytics import YOLO

def start_training(module_name, config_path, model_type="yolov8n.pt", epochs=100):
    """
    Unified training entry point for all specialized CCTV modules.
    """
    print(f"🛠️ Initializing Training for Module: {module_name.upper()}")
    print(f"📊 Using Config: {config_path}")
    
    # Load model
    model = YOLO(model_type)
    
    # Run training
    results = model.train(
        data=config_path,
        epochs=epochs,
        imgsz=640,
        batch=16,
        name=f"cctv_{module_name}",
        augment=True,
        mosaic=1.0, # High importance for small object detection in CCTV
        patience=20
    )
    
    print(f"✅ Training Complete. Model saved to: runs/detect/cctv_{module_name}/weights/best.pt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AIGuard PRO - Unified Training Manager")
    parser.add_argument("--module", type=str, required=True, 
                        help="Module to train (drive_india, plates, fire, behavior)")
    parser.add_argument("--epochs", type=int, default=100)
    args = parser.parse_args()
    
    configs = {
        "drive_india": "training/configs/drive_india.yaml",
        "iruvd": "training/configs/iruvd.yaml",
        "plates": "training/configs/indian_plates.yaml",
        "fire": "training/configs/fire_detection.yaml",
    }
    
    if args.module in configs:
        start_training(args.module, configs[args.module], epochs=args.epochs)
    else:
        print(f"❌ Error: Config for module '{args.module}' not found.")
