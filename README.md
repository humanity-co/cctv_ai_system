# CCTV AI System

Security automation pipeline utilizing convolutional neural networks to detect security events and track object coordinate vectors from live CCTV hardware feeds.

## Technical Architecture
* **Vision Pipeline:** YOLOv8 engine performing object bounding-box regressions and class scoring.
* **Behavior Engine:** Evaluates frame paths to flag behavioral security events.
* **Event Dispatcher:** Fires callback signals and saves video logs upon positive event flags.

## Repository Layout
* `/behavior_detection` - Analyzes positional paths of objects.
* `/pipeline` - Standardizes frame processing, sizing, and inference buffers.
* `/tracking` - Multi-object centroid tracking algorithms.
* `/event_engine` - Signal routers and database triggers.
* `simulate.py` - Synthesizes fake camera environments.

## Setup and Installation
1. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Start CCTV processing:
   ```bash
   python3 simulate.py --source=cctv_sample.mp4
   ```

## License
Proprietary. All rights reserved.
