from ultralytics import YOLO
from pipeline.core import BaseModule
from typing import Dict, Any

class ObjectDetector(BaseModule):
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def process(self, frame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        results = self.model(frame, verbose=False)[0]
        detections = []
        for box in results.boxes:
            detections.append({
                "bbox": box.xyxy[0].tolist(),
                "conf": float(box.conf[0]),
                "class": int(box.cls[0]),
                "label": self.model.names[int(box.cls[0])]
            })
        metadata["detections"] = detections
        return metadata
