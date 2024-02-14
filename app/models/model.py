from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class AppointmentModel(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    id_sucursales: Optional[list[int]] = None
    id_estado_cita: Optional[list[int]] = None