# --- imports section --- #
# pydantic principal data management 
from pydantic import BaseModel
from pydantic import Field
# Libraries for typing configurate
from typing import Literal

class SimpleResponse(BaseModel):
    text_output: str = Field(..., description = "Text response for user request...")


# --- Test para validacion de ejecucion de una tarea de manera seccuencial --- #
class ProgressEvent(BaseModel):
    """Modelo para los eventos de progreso de la herramienta."""
    status: Literal["in_progress", "completed"] = Field(..., description="Estado actual de la tarea.")
    message: str = Field(..., description="Mensaje descriptivo del progreso.")
    percentage: float = Field(..., description="Porcentaje de completitud de la tarea.")

class VideoAnalysis(BaseModel):
    """Modelo para el resultado final del análisis."""
    video_url: str = Field(..., description="URL del video analizado.")
    summary: str = Field(..., description="Resumen del contenido del video.")
    duration_seconds: int = Field(..., description="Duración del video en segundos.")