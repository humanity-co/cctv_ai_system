from pipeline.core import BaseModule
from typing import Dict, Any, List
import time

class BehavioralModule(BaseModule):
    """
    Module for Fire, Smoke, Accident, and Abandoned Object detection.
    """
    def __init__(self):
        self.abandoned_candidates = {} # {track_id: {"first_seen": timestamp, "pos": (x,y)}}

    def process(self, frame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        metadata["environmental_alerts"] = []
        metadata["behavioral_alerts"] = []
        
        objects = metadata.get("tracked_objects", [])
        
        # 1. Prototype Accident Detection
        # Logic: Detect high-velocity overlaps between vehicles
        self._detect_accidents(objects, metadata)
        
        # 2. Abandoned Object Detection
        # Logic: Static object (bag/suitcase) tracked for > 30 seconds
        self._detect_abandoned_objects(objects, metadata)
        
        # 3. Fire / Smoke Detection (Heuristic/Placeholder)
        # In production, this uses a specialized YOLO model (yolov8-fire.pt)
        # We simulate detection if certain keywords are in the demo scenario
        if "fire_demo" in metadata.get("source_name", ""):
            metadata["environmental_alerts"].append({
                "type": "FIRE",
                "confidence": 0.89,
                "message": "🔥 CRITICAL: Fire detected in Sector 4"
            })

        return metadata

    def _detect_accidents(self, objects, metadata):
        # Simulation: If two vehicles are extremely close and have high confidence
        vehicles = [obj for obj in objects if obj["label"] in ["car", "truck", "motorcycle"]]
        for i, v1 in enumerate(vehicles):
            for v2 in vehicles[i+1:]:
                # Check for bounding box overlap (simplified)
                if self._check_overlap(v1["bbox"], v2["bbox"]):
                     metadata["behavioral_alerts"].append({
                        "type": "ACCIDENT",
                        "confidence": 0.75,
                        "message": "💥 ALERT: Possible vehicle collision detected"
                    })

    def _detect_abandoned_objects(self, objects, metadata):
        bags = [obj for obj in objects if obj["label"] in ["bag", "suitcase"]]
        now = time.time()
        for bag in bags:
            tid = bag.get("track_id")
            if tid not in self.abandoned_candidates:
                self.abandoned_candidates[tid] = {"start": now, "pos": bag["bbox"]}
            else:
                duration = now - self.abandoned_candidates[tid]["start"]
                if duration > 10: # 10 seconds for demo
                    metadata["behavioral_alerts"].append({
                        "type": "ABANDONED_OBJECT",
                        "confidence": 0.95,
                        "message": f"⚠️ ALERT: Abandoned bag (ID:{tid}) detected for {int(duration)}s"
                    })

    def _check_overlap(self, b1, b2):
        # Simple intersection check
        return not (b1[2] < b2[0] or b1[0] > b2[2] or b1[3] < b2[1] or b1[1] > b2[3])
