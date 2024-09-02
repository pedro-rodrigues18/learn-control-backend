import base64
import io
import control as ctrl
from matplotlib import pyplot as plt


class BaseController:
    def __init__(
        self, feedback: float, Tf: ctrl.TransferFunction, digital: bool = False
    ):
        self.feedback = feedback
        self.Tf = Tf
        self.digital = digital

    def step_response(self, controller_tf):
        """Plotting the step response of the controller"""
        system_closed_loop = ctrl.feedback(self.Tf * controller_tf, self.feedback)
        time, response = ctrl.step_response(system_closed_loop)

        plt.figure()
        if self.digital:
            plt.step(time, response, where="post")
            plt.xlabel("Amostra")
            plt.ylabel("Resposta")
            plt.title("Resposta ao Degrau - Discreto")
        else:
            plt.plot(time, response)
            plt.xlabel("Tempo (s)")
            plt.ylabel("Resposta")
            plt.title("Resposta ao Degrau")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        step_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return step_base64

    def root_locus(self, controller_tf):
        """Calcula os dados do lugar das raízes (LGR)"""
        system_open_loop = self.Tf * controller_tf

        plt.figure()
        ctrl.root_locus(system_open_loop, plot=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        root_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return root_base64

    def bode_plot(self, controller_tf):
        """Calcula os dados do gráfico de Bode"""
        system_open_loop = self.Tf * controller_tf

        plt.figure()
        ctrl.bode(system_open_loop, plot=True, dB=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        bode_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return bode_base64


class PID(BaseController):
    def __init__(
        self,
        Kp: float,
        Ki: float,
        Kd: float,
        feedback: float,
        Tf: ctrl.TransferFunction,
        digital: bool = False,
    ):
        super().__init__(feedback, Tf, digital)
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def get_controller_tf(self):
        if self.digital:
            return ctrl.TransferFunction(
                [self.Kd, self.Kp, self.Ki], [1, 0, 0], self.Tf.dt
            )
        else:
            return ctrl.TransferFunction([self.Kp, self.Ki, self.Kd], [0, 1, 0])

    def step_response(self):
        return super().step_response(self.get_controller_tf())

    def root_locus(self):
        return super().root_locus(self.get_controller_tf())

    def bode_plot(self):
        return super().bode_plot(self.get_controller_tf())


class PI(BaseController):
    def __init__(
        self,
        Kp: float,
        Ki: float,
        feedback: float,
        Tf: ctrl.TransferFunction,
        digital: bool = False,
    ):
        super().__init__(feedback, Tf, digital)
        self.Kp = Kp
        self.Ki = Ki

    def get_controller_tf(self):
        if self.digital:
            return ctrl.TransferFunction([self.Ki, self.Kp], [1, 0], self.Tf.dt)
        else:
            return ctrl.TransferFunction([self.Kp, self.Ki], [1, 0])

    def step_response(self):
        return super().step_response(self.get_controller_tf())

    def root_locus(self):
        return super().root_locus(self.get_controller_tf())

    def bode_plot(self):
        return super().bode_plot(self.get_controller_tf())


class PD(BaseController):
    def __init__(
        self,
        Kp: float,
        Kd: float,
        feedback: float,
        Tf: ctrl.TransferFunction,
        digital: bool = False,
    ):
        super().__init__(feedback, Tf, digital)
        self.Kp = Kp
        self.Kd = Kd

    def get_controller_tf(self):
        if self.digital:
            return ctrl.TransferFunction([self.Kd, self.Kp], [1], self.Tf.dt)
        else:
            return ctrl.TransferFunction([self.Kd, self.Kp], [0, 1])

    def step_response(self):
        return super().step_response(self.get_controller_tf())

    def root_locus(self):
        return super().root_locus(self.get_controller_tf())

    def bode_plot(self):
        return super().bode_plot(self.get_controller_tf())


class P(BaseController):
    def __init__(
        self,
        Kp: float,
        feedback: float,
        Tf: ctrl.TransferFunction,
        digital: bool = False,
    ):
        super().__init__(feedback, Tf, digital)
        self.Kp = Kp

    def get_controller_tf(self):
        if self.digital:
            return ctrl.TransferFunction([self.Kp], [1], self.Tf.dt)
        else:
            return ctrl.TransferFunction([self.Kp], [1])

    def step_response(self):
        return super().step_response(self.get_controller_tf())

    def root_locus(self):
        return super().root_locus(self.get_controller_tf())

    def bode_plot(self):
        return super().bode_plot(self.get_controller_tf())


class GpNoControlAction(BaseController):
    def __init__(
        self, feedback: float, Tf: ctrl.TransferFunction, digital: bool = False
    ):
        super().__init__(feedback, Tf, digital)

    def step_response(self):
        return super().step_response(
            ctrl.TransferFunction([1], [1])
        )  # Unity feedback for system without control

    def root_locus(self):
        return super().root_locus(
            ctrl.TransferFunction([1], [1])
        )  # Unity feedback for system without control

    def bode_plot(self):
        return super().bode_plot(
            ctrl.TransferFunction([1], [1])
        )  # Unity feedback for system without control


def buildTF(numerator, denominator):
    return ctrl.TransferFunction(numerator, denominator)
