import base64
import io
import control as ctrl
from matplotlib import pyplot as plt


class PID:
    def __init__(
        self,
        Kp: float,
        Ki: float,
        Kd: float,
        feedback: float,
        Tf: ctrl.TransferFunction,
    ):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Plotando a resposta ao degrau do controlador PID no domínio discreto"""
        pid_controller = ctrl.TransferFunction(
            [self.Kd, self.Kp, self.Ki], [1, 0, 0], self.Tf.dt
        )
        system_pid_closed_loop = ctrl.feedback(self.Tf * pid_controller, self.feedback)

        time_pid, response_pid = ctrl.step_response(system_pid_closed_loop)

        plt.figure()
        plt.step(
            time_pid, response_pid, where="post"
        )  # Use plt.step para o domínio discreto
        plt.xlabel("Amostra")
        plt.ylabel("Resposta")
        plt.title("Resposta ao Degrau - PID Discreto")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        step_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return step_base64

    def root_locus(self):
        """Calcula o lugar das raízes do sistema PID no domínio discreto"""
        pid_controller = ctrl.TransferFunction(
            [self.Kd, self.Kp, self.Ki], [1, 0, 0], self.Tf.dt
        )
        system_pid_open_loop = self.Tf * pid_controller

        plt.figure()
        ctrl.root_locus(system_pid_open_loop, plot=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        root_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return root_base64

    def bode_plot(self):
        """Calcula o gráfico de Bode do sistema PID no domínio discreto"""
        pid_controller = ctrl.TransferFunction(
            [self.Kd, self.Kp, self.Ki], [1, 0, 0], self.Tf.dt
        )
        system_pid_open_loop = self.Tf * pid_controller

        plt.figure()
        ctrl.bode(system_pid_open_loop, plot=True, dB=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        bode_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return bode_base64


class PI:
    def __init__(
        self, Kp: float, Ki: float, feedback: float, Tf: ctrl.TransferFunction
    ):
        self.Kp = Kp
        self.Ki = Ki
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Plotando a resposta ao degrau do controlador PI no domínio discreto"""
        pi_controller = ctrl.TransferFunction([self.Ki, self.Kp], [1, 0], self.Tf.dt)
        system_pi_closed_loop = ctrl.feedback(self.Tf * pi_controller, self.feedback)

        time_pi, response_pi = ctrl.step_response(system_pi_closed_loop)

        plt.figure()
        plt.step(
            time_pi, response_pi, where="post"
        )  # Use plt.step para o domínio discreto
        plt.xlabel("Amostra")
        plt.ylabel("Resposta")
        plt.title("Resposta ao Degrau - PI Discreto")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        step_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return step_base64

    def root_locus(self):
        """Calcula o lugar das raízes do sistema PI no domínio discreto"""
        pi_controller = ctrl.TransferFunction([self.Ki, self.Kp], [1, 0], self.Tf.dt)
        system_pi_open_loop = self.Tf * pi_controller

        plt.figure()
        ctrl.root_locus(system_pi_open_loop, plot=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        root_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return root_base64

    def bode_plot(self):
        """Calcula o gráfico de Bode do sistema PI no domínio discreto"""
        pi_controller = ctrl.TransferFunction([self.Ki, self.Kp], [1, 0], self.Tf.dt)
        system_pi_open_loop = self.Tf * pi_controller

        plt.figure()
        ctrl.bode(system_pi_open_loop, plot=True, dB=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        bode_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return bode_base64


class PD:
    def __init__(
        self, Kp: float, Kd: float, feedback: float, Tf: ctrl.TransferFunction
    ):
        self.Kp = Kp
        self.Kd = Kd
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Plotando a resposta ao degrau do controlador PD no domínio discreto"""
        pd_controller = ctrl.TransferFunction([self.Kd, self.Kp], [1], self.Tf.dt)
        system_pd_closed_loop = ctrl.feedback(self.Tf * pd_controller, self.feedback)

        time_pd, response_pd = ctrl.step_response(system_pd_closed_loop)

        plt.figure()
        plt.step(
            time_pd, response_pd, where="post"
        )  # Use plt.step para o domínio discreto
        plt.xlabel("Amostra")
        plt.ylabel("Resposta")
        plt.title("Resposta ao Degrau - PD Discreto")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        step_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return step_base64

    def root_locus(self):
        """Calcula o lugar das raízes do sistema PD no domínio discreto"""
        pd_controller = ctrl.TransferFunction([self.Kd, self.Kp], [1], self.Tf.dt)
        system_pd_open_loop = self.Tf * pd_controller

        plt.figure()
        ctrl.root_locus(system_pd_open_loop, plot=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        root_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return root_base64

    def bode_plot(self):
        """Calcula o gráfico de Bode do sistema PD no domínio discreto"""
        pd_controller = ctrl.TransferFunction([self.Kd, self.Kp], [1], self.Tf.dt)
        system_pd_open_loop = self.Tf * pd_controller

        plt.figure()
        ctrl.bode(system_pd_open_loop, plot=True, dB=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        bode_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return bode_base64


class P:
    def __init__(self, Kp: float, feedback: float, Tf: ctrl.TransferFunction):
        self.Kp = Kp
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Plotando a resposta ao degrau do controlador P no domínio discreto"""
        p_controller = ctrl.TransferFunction([self.Kp], [1], self.Tf.dt)
        system_p_closed_loop = ctrl.feedback(self.Tf * p_controller, self.feedback)

        time_p, response_p = ctrl.step_response(system_p_closed_loop)

        plt.figure()
        plt.step(
            time_p, response_p, where="post"
        )  # Use plt.step para o domínio discreto
        plt.xlabel("Amostra")
        plt.ylabel("Resposta")
        plt.title("Resposta ao Degrau - P Discreto")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        step_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return step_base64

    def root_locus(self):
        """Calcula o lugar das raízes do sistema P no domínio discreto"""
        p_controller = ctrl.TransferFunction([self.Kp], [1], self.Tf.dt)
        system_p_open_loop = self.Tf * p_controller

        plt.figure()
        ctrl.root_locus(system_p_open_loop, plot=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        root_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return root_base64

    def bode_plot(self):
        """Calcula o gráfico de Bode do sistema P no domínio discreto"""
        p_controller = ctrl.TransferFunction([self.Kp], [1], self.Tf.dt)
        system_p_open_loop = self.Tf * p_controller

        plt.figure()
        ctrl.bode(system_p_open_loop, plot=True, dB=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        bode_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return bode_base64


class GpNoControlAction:
    def __init__(self, feedback: float, Tf: ctrl.TransferFunction):
        self.Tf = Tf
        self.feedback = feedback

    def step_response(self):
        """Plotando a resposta ao degrau do sistema sem ação de controle no domínio discreto"""
        tf_closed_layer = ctrl.feedback(self.Tf, self.feedback)
        time_gp, response_gp = ctrl.step_response(tf_closed_layer)

        plt.figure()
        plt.step(
            time_gp, response_gp, where="post"
        )  # Use plt.step para o domínio discreto
        plt.xlabel("Amostra")
        plt.ylabel("Resposta")
        plt.title("Resposta ao Degrau - Sem Controle Discreto")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        step_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return step_base64

    def root_locus(self):
        """Calcula o lugar das raízes do sistema sem ação de controle no domínio discreto"""
        system_open_loop = self.Tf

        plt.figure()
        ctrl.root_locus(system_open_loop, plot=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        root_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return root_base64

    def bode_plot(self):
        """Calcula o gráfico de Bode do sistema sem ação de controle no domínio discreto"""
        system_open_loop = self.Tf

        plt.figure()
        ctrl.bode(system_open_loop, plot=True, dB=True)
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        bode_base64 = base64.b64encode(buf.read()).decode("utf-8")
        return bode_base64
