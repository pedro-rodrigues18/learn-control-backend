from typing import List
from pydantic import BaseModel


class ControlResponse(BaseModel):
    time: List[float]
    response: List[float]
