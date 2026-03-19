from typing import Dict, Any, List

class EventReasoningEngine:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            "restricted_zones": [],
            "max_crowd_density": 10,
            "suspicious_loiter_time": 60, # seconds
        }

    def evaluate(self, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        alerts = []
        objects = metadata.get("tracked_objects", [])
        
        # 1. Intrusion Detection (Restricted Zone)
        for obj in objects:
            if self._is_in_restricted_zone(obj):
                alerts.append({
                    "type": "intrusion",
                    "message": f"Intrusion detected: {obj['label']} in restricted zone.",
                    "confidence": obj["conf"],
                    "timestamp": metadata["timestamp"]
                })

        # 2. Crowd Density
        persons = [obj for obj in objects if obj["label"] == "person"]
        if len(persons) > self.config["max_crowd_density"]:
            alerts.append({
                "type": "crowd_alert",
                "message": f"High crowd density: {len(persons)} persons detected.",
                "confidence": 0.9,
                "timestamp": metadata["timestamp"]
            })

        # 3. Unknown Person
        for face in metadata.get("faces", []):
            if face.get("is_unknown", False):
                alerts.append({
                    "type": "unknown_person",
                    "message": "Unknown person detected at front entrance.",
                    "confidence": face["conf"],
                    "timestamp": metadata["timestamp"]
                })

        return alerts

    def _is_in_restricted_zone(self, obj):
        # Simplified geometry logic for prototype
        return False
