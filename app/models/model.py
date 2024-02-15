from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class AppointmentModel(BaseModel):
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    id_sucursales: list[int] | None = None
    id_estado_cita: list[int] | None = None

class StateAppointmentModel(BaseModel):
    id_cita: int = Field(..., description="Id de la cita")
    id_estado: int = Field(..., description="Estado de la cita")
    comentarios: str = Field(..., description="Comentarios del cambio de estado")