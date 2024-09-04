from fastapi import FastAPI, WebSocket
from services.pid_service import PID, PI, PD, P, GpNoControlAction, buildTF
from schemas.values_scheme import Values
from fastapi.middleware.cors import CORSMiddleware
from control.matlab import c2d

app = FastAPI()

control = ""
current_values = {}
connected_clients = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/send_values")
async def control_system(values: Values):

    for key, value in values.dict().items():
        if value is not None:
            current_values[key] = value

    for client in connected_clients:
        await client.send_json(current_values)

    return {
        "success": True,
        "message": "Data sent successfully",
        "data": current_values,
    }


@app.get("/get_values")
async def get_values():
    return {
        "success": True,
        "message": "Success",
        "data": current_values,
    }


def get_controller(control_type, transfer_function, digital=False):
    """Função auxiliar para instanciar o controlador correto."""
    if control_type == "pid":
        return PID(
            Kp=current_values["kp"],
            Ki=current_values["ki"],
            Kd=current_values["kd"],
            feedback=1,
            Tf=transfer_function,
            digital=digital,
        )
    elif control_type == "pi":
        return PI(
            Kp=current_values["kp"],
            Ki=current_values["ki"],
            feedback=1,
            Tf=transfer_function,
            digital=digital,
        )
    elif control_type == "pd":
        return PD(
            Kp=current_values["kp"],
            Kd=current_values["kd"],
            feedback=1,
            Tf=transfer_function,
            digital=digital,
        )
    elif control_type == "p":
        return P(
            Kp=current_values["kp"],
            feedback=1,
            Tf=transfer_function,
            digital=digital,
        )
    elif control_type == "gp_no_control_action":
        return GpNoControlAction(
            feedback=1,
            Tf=transfer_function,
            digital=digital,
        )
    else:
        return None


@app.get("/continuo/{control_type}")
async def continuo_endpoint(control_type: str, tau: float):
    global current_values
    transfer_function = buildTF([1], [tau, 1])
    print(transfer_function)

    controller = get_controller(control_type, transfer_function)

    if controller is None:
        return {"error": "Invalid control type"}

    step_response = controller.step_response()
    root_locus = controller.root_locus()
    bode_plot = controller.bode_plot()

    current_values["plot"] = False

    return {
        "control_type": control_type,
        "step_response": step_response,
        "root_locus": root_locus,
        "bode_plot": bode_plot,
    }


@app.get("/digital/{control_type}")
async def digital_endpoint(control_type: str, sample_time: float, tau: float):
    global current_values
    transfer_function = buildTF([1], [tau, 1])
    transfer_function = c2d(transfer_function, sample_time, method="zoh")
    print(transfer_function)

    controller = get_controller(control_type, transfer_function, digital=True)

    if controller is None:
        return {"error": "Invalid control type"}

    step_response = controller.step_response()
    root_locus = controller.root_locus()
    bode_plot = controller.bode_plot()

    current_values["plot"] = False

    return {
        "control_type": control_type,
        "step_response": step_response,
        "root_locus": root_locus,
        "bode_plot": bode_plot,
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
