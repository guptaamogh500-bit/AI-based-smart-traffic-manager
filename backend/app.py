from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI(title="UrbanFlow Integration Hub")

# 1. Bypass Browser Security Blocks (Fixes the 403 Error)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. WebSocket Manager to Push Data to Dashboard
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                pass

manager = ConnectionManager()

# 3. Handle Live UI Connections (Fixes WebSocket 403 Error)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 4. Handle HTTP Fallback (Fixes 404 Error)
@app.get("/signals/state")
async def get_state():
    return {"status": "active"}

# 5. Receive AI Data & Broadcast to UI
@app.post("/api/traffic/update-density")
async def update_density(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
        
    total_vehicles = 0
    
    # 1. If it's a list (like your AI is sending), sum up the vehicle_counts
    if isinstance(data, list):
        total_vehicles = sum(lane.get("vehicle_count", 0) for lane in data if isinstance(lane, dict))
    
    # 2. Backup just in case it sends a dictionary
    elif isinstance(data, dict):
        total_vehicles = data.get("total_vehicles", 0)
        if total_vehicles == 0:
            total_vehicles = sum(v for k, v in data.items() if isinstance(v, (int, float)))
            
    print(f"Received from AI: {data} --> Broadcasting: {int(total_vehicles)}")
        
    # Push the live total count to the frontend!
    await manager.broadcast({"total_vehicles": int(total_vehicles)})
    return {"status": "success"}

@app.post("/api/update-density")
@app.post("/update-density")
async def fallback_density(request: Request):
    return await update_density(request)

@app.post("/update-density")
async def fallback_density(data: dict):
    return await update_density(data)