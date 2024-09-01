import control as ctrl
from schemas.control_schema import ControlResponse


class PID:
    def __init__(self, Kp: float, Ki: float, Kd: float, feedback: float, Tf: ctrl.tf):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Ploting the step response of the PID controller"""
        # Calculando a função de transferência da malha fechada com o controlador PID
        pid_controller = ctrl.TransferFunction([self.Kp, self.Ki, self.Kd], [0, 1, 0])
        system_pid_closed_loop = ctrl.feedback(self.Tf * pid_controller, self.feedback)

        # Obtendo a resposta ao degrau da malha fechada
        time_pid, response_pid = ctrl.step_response(system_pid_closed_loop)

        return ControlResponse(time=time_pid.tolist(), response=response_pid.tolist())

    def root_locus(self):
        """Calcula os dados do lugar das raízes (LGR)"""
        pid_controller = ctrl.TransferFunction([self.Kp, self.Ki, self.Kd], [0, 1, 0])
        system_pid_open_loop = self.Tf * pid_controller
        root_locus_data = ctrl.root_locus(system_pid_open_loop)

        print(root_locus_data)

        rlist = root_locus_data[0]
        klist = root_locus_data[1]

        print(rlist)
        print(klist)

        breakpoint()

        return {"rlist": [r.tolist() for r in rlist], "klist": klist.tolist()}

    def bode_plot(self):
        """Calcula os dados do gráfico de Bode"""
        pid_controller = ctrl.TransferFunction([self.Kp, self.Ki, self.Kd], [0, 1, 0])
        system_pid_open_loop = self.Tf * pid_controller

        mag, phase, omega = ctrl.bode(system_pid_open_loop, plot=False, dB=True)

        return {
            "magnitude": mag.tolist(),
            "phase": phase.tolist(),
            "omega": omega.tolist(),
        }


class PI:
    def __init__(self, Kp: float, Ki: float, feedback: float, Tf: ctrl.tf):
        self.Kp = Kp
        self.Ki = Ki
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Ploting the step response of the PI controller"""
        pi_controller = ctrl.TransferFunction([self.Kp, self.Ki], [1, 0])
        system_pi_closed_loop = ctrl.feedback(self.Tf * pi_controller, self.feedback)

        time_pi, response_pi = ctrl.step_response(system_pi_closed_loop)

        return ControlResponse(time=time_pi.tolist(), response=response_pi.tolist())

    def root_locus(self):
        """Calcula os dados do lugar das raízes (LGR)"""
        pi_controller = ctrl.TransferFunction([self.Kp, self.Ki], [1, 0])
        system_pi_open_loop = self.Tf * pi_controller

        rlist, klist = ctrl.root_locus(system_pi_open_loop)

        return {"rlist": [r.tolist() for r in rlist], "klist": klist.tolist()}

    def bode_plot(self):
        """Calcula os dados do gráfico de Bode"""
        pi_controller = ctrl.TransferFunction([self.Kp, self.Ki], [1, 0])
        system_pi_open_loop = self.Tf * pi_controller

        mag, phase, omega = ctrl.bode(system_pi_open_loop, plot=False, dB=True)

        return {
            "magnitude": mag.tolist(),
            "phase": phase.tolist(),
            "omega": omega.tolist(),
        }


class PD:
    def __init__(self, Kp: float, Kd: float, feedback: float, Tf: ctrl.tf):
        self.Kp = Kp
        self.Kd = Kd
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Ploting the step response of the PD controller"""
        pd_controller = ctrl.TransferFunction([self.Kd, self.Kp], [0, 1])
        system_pd_closed_loop = ctrl.feedback(self.Tf * pd_controller, self.feedback)

        time_pd, response_pd = ctrl.step_response(system_pd_closed_loop)

        return ControlResponse(time=time_pd.tolist(), response=response_pd.tolist())

    def root_locus(self):
        """Calcula os dados do lugar das raízes (LGR)"""
        pd_controller = ctrl.TransferFunction([self.Kd, self.Kp], [0, 1])
        system_pd_open_loop = self.Tf * pd_controller

        rlist, klist = ctrl.root_locus(system_pd_open_loop)

        return {"rlist": [r.tolist() for r in rlist], "klist": klist.tolist()}

    def bode_plot(self):
        """Calcula os dados do gráfico de Bode"""
        pd_controller = ctrl.TransferFunction([self.Kd, self.Kp], [0, 1])
        system_pd_open_loop = self.Tf * pd_controller

        mag, phase, omega = ctrl.bode(system_pd_open_loop, plot=False, dB=True)

        return {
            "magnitude": mag.tolist(),
            "phase": phase.tolist(),
            "omega": omega.tolist(),
        }


class P:
    def __init__(self, Kp: float, feedback: float, Tf: ctrl.tf):
        self.Kp = Kp
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Ploting the step response of the P controller"""
        p_controller = ctrl.TransferFunction([self.Kp], [1])
        system_p_closed_loop = ctrl.feedback(self.Tf * p_controller, self.feedback)

        time_p, response_p = ctrl.step_response(system_p_closed_loop)

        return ControlResponse(time=time_p.tolist(), response=response_p.tolist())

    def root_locus(self):
        """Calcula os dados do lugar das raízes (LGR)"""
        p_controller = ctrl.TransferFunction([self.Kp], [1])
        system_p_open_loop = self.Tf * p_controller

        rlist, klist = ctrl.root_locus(system_p_open_loop)

        return {"rlist": [r.tolist() for r in rlist], "klist": klist.tolist()}

    def bode_plot(self):
        """Calcula os dados do gráfico de Bode"""
        p_controller = ctrl.TransferFunction([self.Kp], [1])
        system_p_open_loop = self.Tf * p_controller

        mag, phase, omega = ctrl.bode(system_p_open_loop, plot=False, dB=True)

        return {
            "magnitude": mag.tolist(),
            "phase": phase.tolist(),
            "omega": omega.tolist(),
        }


class GpNoControlAction:
    def __init__(self, feedback: float, Tf: ctrl.tf):
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Ploting the step response of the system without control action"""
        tf_closed_layer = ctrl.feedback(self.Tf, self.feedback)
        time_gp, response_gp = ctrl.step_response(tf_closed_layer)

        return ControlResponse(time=time_gp.tolist(), response=response_gp.tolist())

    def root_locus(self):
        """Calcula os dados do lugar das raízes (LGR)"""
        system_open_loop = self.Tf

        rlist, klist = ctrl.root_locus(system_open_loop)

        return {"rlist": [r.tolist() for r in rlist], "klist": klist.tolist()}

    def bode_plot(self):
        """Calcula os dados do gráfico de Bode"""
        system_open_loop = self.Tf

        mag, phase, omega = ctrl.bode(system_open_loop, plot=False, dB=True)

        return {
            "magnitude": mag.tolist(),
            "phase": phase.tolist(),
            "omega": omega.tolist(),
        }


def buildTF(numerator, denominator):
    return ctrl.tf(numerator, denominator)
