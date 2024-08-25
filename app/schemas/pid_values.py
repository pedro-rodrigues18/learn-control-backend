from pydantic import BaseModel

class PIDValues(BaseModel):
    """
    Class to represent the PID constants for the controller

    Attributes:
        kp: float
            Proportional constant
        ki: float
            Integral constant
        kd: float
            Derivative constant
    """
    kp: float
    ki: float
    kd: float
