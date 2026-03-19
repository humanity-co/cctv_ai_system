import cv2
import numpy as np
import time
from pipeline.core import MLPipeline, VideoStreamHandler
from pipeline.detection import ObjectDetector
from tracking.bytetrack import ByteTracker

def run_webcam_demo():
    """Captures from webcam and runs the actual ML pipeline with visual overlays."""
    print("🚀 Initializing AI CCTV Webcam Demo...")
    
    # Initialize real modules
    detector = ObjectDetector()
    tracker = ByteTracker()
    pipeline = MLPipeline([detector, tracker])
    
    # Source 0 is usually the built-in webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    print("✅ Webcam connected. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process frame through the real AI pipeline
        _, metadata = pipeline.run_on_frame(frame)
        
        # Draw detections
        for obj in metadata.get("tracked_objects", []):
            bbox = obj["bbox"]
            label = f"{obj['label']} ID:{obj.get('track_id', '?')}"
            
            # Draw box (Neon Blue)
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 242, 0), 2)
            
            # Draw label
            cv2.putText(frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 242, 0), 2)

        # UI Overlay
        cv2.putText(frame, f"AIGuard Live - {time.strftime('%H:%M:%S')}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("AIGuard Live AI Stream", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_webcam_demo()
