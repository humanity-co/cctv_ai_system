import cv2
import time
import threading
from pipeline.core import MLPipeline, VideoStreamHandler
from pipeline.detection import ObjectDetector
from tracking.bytetrack import ByteTracker
from event_engine.reasoner import EventReasoningEngine

class PipelineManager:
    def __init__(self):
        # Initialize modules
        self.detector = ObjectDetector()
        self.tracker = ByteTracker()
        self.reasoner = EventReasoningEngine()
        
        # Create pipeline
        self.pipeline = MLPipeline([
            self.detector,
            self.tracker,
            # face_recog, ocr would go here
        ])
        
        self.active_streams = {}
        self.alerts_history = []

    def start_stream(self, camera_id, source):
        if camera_id in self.active_streams:
            return
        
        handler = VideoStreamHandler(source)
        thread = threading.Thread(target=self._process_stream, args=(camera_id, handler))
        thread.daemon = True
        self.active_streams[camera_id] = {"thread": thread, "running": True}
        thread.start()

    def _process_stream(self, camera_id, handler):
        print(f"Starting processing for camera {camera_id}")
        for frame in handler.get_frames():
            if not self.active_streams.get(camera_id, {}).get("running"):
                break
                
            frame, metadata = self.pipeline.run_on_frame(frame)
            metadata["camera_id"] = camera_id
            
            # Reasoning
            new_alerts = self.reasoner.evaluate(metadata)
            if new_alerts:
                self.alerts_history.extend(new_alerts)
                # In production: save to DB and notify via Redis/WS
                for alert in new_alerts:
                    print(f"ALERT [{camera_id}]: {alert['message']}")

    def stop_stream(self, camera_id):
        if camera_id in self.active_streams:
            self.active_streams[camera_id]["running"] = False
            del self.active_streams[camera_id]
