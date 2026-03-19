import cv2
import time
from pipeline.core import MLPipeline
from pipeline.detection import ObjectDetector
from tracking.bytetrack import ByteTracker
from pipeline.indian_context import IndianANPR, IndianFaceID
from behavior_detection.behavior import BehavioralModule

def process_cctv_video(video_path="datasets/scenarios/traffic.mp4", output_path="datasets/analysis_output.mp4"):
    """Runs the AI pipeline on a recorded CCTV video file."""
    print(f"🚀 Processing CCTV Video: {video_path}")
    
    # SOTA Weights: Professional UVH-26 model trained on Indian Traffic
    sota_weights = "datasets/drive_india/uvh26/weights/YOLOv11-S/UVH-26-MV-YOLOv11-S.pt"
    
    # Initialize ML modules
    detector = ObjectDetector(model_path=sota_weights)
    tracker = ByteTracker()
    indian_anpr = IndianANPR()
    indian_face = IndianFaceID()
    behavior_mod = BehavioralModule()
    
    pipeline = MLPipeline([detector, tracker, indian_anpr, indian_face, behavior_mod])
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Error: Could not open video file {video_path}")
        return

    # Get video properties for output
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"✅ Video loaded: {width}x{height} @ {fps} FPS.")
    print(f"📽️ Saving analysis to: {output_path}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Run AI Pipeline
        current_metadata = {"source_name": video_path}
        _, metadata = pipeline.run_on_frame(frame)
        metadata.update(current_metadata)
        
        # Visualize Detections
        for obj in metadata.get("tracked_objects", []):
            x1, y1, x2, y2 = map(int, obj["bbox"])
            label = f"{obj['label']} #{obj.get('track_id', '?')}"
            
            # Draw Bounding Box (Neon Pink)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Draw Global Alerts (Fire, Accidents, etc.)
        all_alerts = metadata.get("environmental_alerts", []) + metadata.get("behavioral_alerts", [])
        for i, alert in enumerate(all_alerts):
            cv2.putText(frame, alert["message"], (20, 110 + (i*30)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Dashboard-style Overlay
        cv2.putText(frame, "AIGuard PRO - SOTA MODE (UVH-26)", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"CAM_REPLAY_01 | {time.strftime('%Y-%m-%d %H:%M:%S')}", (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Save Frame
        out.write(frame)
        
        # Optional Window Display
        # cv2.imshow("AIGuard CCTV Video Analysis", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    out.release()
    # cv2.destroyAllWindows()
    print(f"✅ Analysis complete. File saved: {output_path}")
    print("✅ Video processing complete.")

if __name__ == "__main__":
    process_cctv_video()
