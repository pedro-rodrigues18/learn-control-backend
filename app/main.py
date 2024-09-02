from fastapi import FastAPI, WebSocket
from services.pid_service import *
import services.pid_digital_service as ds
from schemas.pid_values import PIDValues
from fastapi.middleware.cors import CORSMiddleware
from control.matlab import c2d

app = FastAPI()

current_values = {"kp": 0.0, "ki": 0.0, "kd": 0.0}
connected_clients = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/send_values")
async def control_system(values: PIDValues):
    global current_values

    current_values = {"kp": values.kp, "ki": values.ki, "kd": values.kd}

    for client in connected_clients:
        await client.send_json(current_values)

    return {"success": True, "message": "Data sent successfully"}


@app.get("/continuo/{control_type}")
async def continuo_endpoint(control_type: str, tau: float):
    global current_values
    transfer_function = buildTF([1], [tau, 1])

    print(transfer_function)

    if control_type == "pid":
        pid = PID(
            Kp=current_values["kp"],
            Ki=current_values["ki"],
            Kd=current_values["kd"],
            feedback=1,
            Tf=transfer_function,
        )
        step_response = pid.step_response()
        root_locus = pid.root_locus()
        bode_plot = pid.bode_plot()
    elif control_type == "pi":
        pi = PI(
            Kp=current_values["kp"],
            Ki=current_values["ki"],
            feedback=1,
            Tf=transfer_function,
        )
        step_response = pi.step_response()
        root_locus = pi.root_locus()
        bode_plot = pi.bode_plot()
    elif control_type == "pd":
        pd = PD(
            Kp=current_values["kp"],
            Kd=current_values["kd"],
            feedback=1,
            Tf=transfer_function,
        )
        step_response = pd.step_response()
        root_locus = pd.root_locus()
        bode_plot = pd.bode_plot()
    elif control_type == "p":
        p = P(Kp=current_values["kp"], feedback=1, Tf=transfer_function)
        step_response = p.step_response()
        root_locus = p.root_locus()
        bode_plot = p.bode_plot()
    elif control_type == "gp_no_control_action":
        gp_no_control_action = GpNoControlAction(feedback=1, Tf=transfer_function)
        step_response = gp_no_control_action.step_response()
        root_locus = gp_no_control_action.root_locus()
        bode_plot = gp_no_control_action.bode_plot()
    else:
        return {"error": "Invalid control type"}

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
    transfer_function = c2d(transfer_function, sample_time, method="tustin")

    print(transfer_function)

    if control_type == "pid":
        pid = ds.PID(
            Kp=current_values["kp"],
            Ki=current_values["ki"],
            Kd=current_values["kd"],
            feedback=1,
            Tf=transfer_function,
        )
        step_response = pid.step_response()
        root_locus = pid.root_locus()
        bode_plot = pid.bode_plot()
    elif control_type == "pi":
        pi = ds.PI(
            Kp=current_values["kp"],
            Ki=current_values["ki"],
            feedback=1,
            Tf=transfer_function,
        )
        step_response = pi.step_response()
        root_locus = pi.root_locus()
        bode_plot = pi.bode_plot()
    elif control_type == "pd":
        pd = ds.PD(
            Kp=current_values["kp"],
            Kd=current_values["kd"],
            feedback=1,
            Tf=transfer_function,
        )
        step_response = pd.step_response()
        root_locus = pd.root_locus()
        bode_plot = pd.bode_plot()
    elif control_type == "p":
        p = ds.P(Kp=current_values["kp"], feedback=1, Tf=transfer_function)
        step_response = p.step_response()
        root_locus = p.root_locus()
        bode_plot = p.bode_plot()
    elif control_type == "gp_no_control_action":
        gp_no_control_action = ds.GpNoControlAction(feedback=1, Tf=transfer_function)
        step_response = gp_no_control_action.step_response()
        root_locus = gp_no_control_action.root_locus()
        bode_plot = gp_no_control_action.bode_plot()
    else:
        return {"error": "Invalid control type"}

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
