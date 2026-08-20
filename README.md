# AI-based-smart-traffic-manager
UrbanFlow — AI-Based Smart Traffic Manager
UrbanFlow is an Adaptive Traffic Control System (ATCS) that leverages real-time computer vision to dynamically adjust traffic signal timings based on live vehicle density. By replacing fixed-timer traffic lights with AI-driven adaptive logic, this system minimizes wait times, reduces congestion, and optimizes intersection throughput.

System Architecture
The project is divided into three decoupled microservices working in tandem:

AI Vision Pipeline (/ai): Utilizes the UVH-26-MV-YOLOv11-S model for high-speed object detection alongside ByteTrack for occlusion-proof vehicle tracking across video frames.

FastAPI Integration Hub (/backend): A lightweight Python backend that ingests raw JSON telemetry from the AI pipeline and instantly broadcasts it to the frontend via WebSockets.

Real-Time Dashboard (/dashboard): A responsive HTML5/JS interface featuring a live intersection map, dynamic Chart.js throughput graphs, and an adaptive countdown timer.

Features
Dynamic Signal Timing: Calculates green-light duration continuously using a 2-second-per-vehicle multiplier (bounded between 15s and 90s) rather than relying on static cycles.

Live Edge-to-Cloud Sync: Uses WebSocket connections (with HTTP fallback) to guarantee sub-second latency between camera detection and dashboard visualization.

Multi-Lane Tracking: Processes independent video feeds (North, South, East, West) simultaneously to aggregate a comprehensive junction density score.

Resilient Tracking: Integrates ByteTrack to maintain accurate unique vehicle IDs even through heavy occlusion, preventing double-counting in dense traffic.

Tech Stack
Computer Vision: YOLOv11, ByteTrack, OpenCV, NumPy

Backend: Python 3.12.11, FastAPI, Uvicorn, WebSockets

Frontend: HTML, CSS, Vanilla JavaScript, Chart.js

STRUCTURE : 

AI-based-smart-traffic-manager/
├── ai/                     # YOLO detection loop and ByteTrack logic
│   ├── detection/          # Model configuration and class definitions
│   └── main.py             # Vision pipeline entry point
├── backend/                # FastAPI server hub
│   ├── models/             # Data validation schemas
│   ├── routes/             # API and WebSocket endpoints
│   ├── services/           # Core signal calculation logic
│   └── app.py              # Uvicorn server entry point
├── dashboard/              # Web interface
│   ├── script.js           # Live WebSocket ingestion and adaptive timer
│   ├── style.css           # UI styling
│   └── urbanflow.html      # Main dashboard view
└── data/videos/            # Input streams (east.mp4, north.mp4, etc.)