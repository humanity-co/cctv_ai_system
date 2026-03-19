import cv2
import time
import os
from ultralytics import YOLO

def generate_demo(model_path="runs/detect/cctv_iruvd/weights/best.pt", video_path="datasets/scenarios/traffic.mp4", output_path="datasets/demo_finetuned_output.mp4"):
    print(f"🚀 Loading Fine-tuned Model: {model_path}")
    model = YOLO(model_path)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Error: Could not open video {video_path}")
        return

    # Video writer setup
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"📽️ Processing video and saving to {output_path}...")
    
    frame_count = 0
    max_frames = 150 # Process first ~5-10 seconds for a quick demo
    
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        results = model(frame, verbose=False)[0]
        
        # Draw detections
        for box in results.boxes:
            b = box.xyxy[0].tolist()
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = f"{model.names[cls]} {conf:.2f}"
            
            # Use specific colors for Indian classes
            color = (0, 255, 0) # Default Green
            if "rickshaw" in model.names[cls].lower() or "toto" in model.names[cls].lower():
                color = (0, 215, 255) # Gold/Yellow for Rickshaws
            
            cv2.rectangle(frame, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), color, 2)
            cv2.putText(frame, label, (int(b[0]), int(b[1]) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Overlay Info
        cv2.putText(frame, "AIGuard PRO - FINE-TUNED (IRUVD)", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        out.write(frame)
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"⏳ Processed {frame_count} frames...")

    cap.release()
    out.release()
    print(f"✅ Demo video generated: {output_path}")

if __name__ == "__main__":
    generate_demo()
