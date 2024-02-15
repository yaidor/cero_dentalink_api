from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class AppointmentModel(BaseModel):
    ini_date: date | None = None
    end_date: date | None = None
    id_state: list[int] | None = None
    id_office: list[int] | None = None

class StateAppointmentModel(BaseModel):
    id_appointment: int = Field(..., description="ID of the appointment")
    id_state: int = Field(..., description="ID of the new state of the appointment")
    comments: str = Field(..., description="Comments of the state change")