from typing import Optional
from pydantic import BaseModel


class Values(BaseModel):
    """
    Class to represent the PID constant for the controller

    Attributes:
        ki: float
        kp: float
        kd: float
        tau: float
        ts: float
    """

    control: Optional[str] = None
    control_type: Optional[str] = None
    ki: Optional[float] = None
    kp: Optional[float] = None
    kd: Optional[float] = None
    tau: Optional[float] = None
    ts: Optional[float] = None
    plot: Optional[bool] = False
