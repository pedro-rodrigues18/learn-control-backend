from fastapi import FastAPI, WebSocket
from schemas.pid_values import PIDValues

app = FastAPI()

current_values = {"kp": 0.0, "ki": 0.0, "kd": 0.0}
connected_clients = []

@app.post("/send_values")
async def control_system(values: PIDValues):
    global current_values
    current_values = {"kp": values.kp, "ki": values.ki, "kd": values.kd}

    for client in connected_clients:
        await client.send_json(current_values)

    return {
        "kp": values.kp,
        "ki": values.ki,
        "kd": values.kd,
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"Client disconnected: {e}")
    finally:
        connected_clients.remove(websocket)
