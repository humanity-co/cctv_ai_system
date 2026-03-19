import cv2
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseModule(ABC):
    @abstractmethod
    def process(self, frame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Process a frame and return updated metadata."""
        pass

class MLPipeline:
    def __init__(self, modules: List[BaseModule]):
        self.modules = modules

    def run_on_frame(self, frame):
        metadata = {"timestamp": time.time()}
        for module in self.modules:
            metadata = module.process(frame, metadata)
        return frame, metadata

class VideoStreamHandler:
    def __init__(self, source):
        self.source = source
        self.cap = cv2.VideoCapture(source)

    def get_frames(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            yield frame
        self.cap.release()
