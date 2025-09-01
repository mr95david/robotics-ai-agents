from pydantic_ai import Agent
# from pydantic_ai import tool
from pydantic import BaseModel, Field
from typing import Literal
import asyncio
from typing import AsyncGenerator

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

async def analyze_video(video_url: str) -> AsyncGenerator[ProgressEvent, None]:
    """
    Analiza un video de forma asíncrona y emite eventos de progreso.
    """
    print(f"Iniciando el análisis del video: {video_url}")

    # Simulación del inicio
    yield ProgressEvent(status="in_progress", message="Iniciando descarga del video...", percentage=10.0)
    await asyncio.sleep(2)

    # Simulación del procesamiento
    yield ProgressEvent(status="in_progress", message="Extrayendo fotogramas clave...", percentage=50.0)
    await asyncio.sleep(3)

    # Simulación de la finalización
    yield ProgressEvent(status="in_progress", message="Análisis de contenido finalizado, generando resumen...", percentage=90.0)
    await asyncio.sleep(2)

    # Evento final
    yield ProgressEvent(status="completed", message="Análisis completado exitosamente.", percentage=100.0)



# Envolver la función en la herramienta que el agente puede usar


# Crear el agente
agent = Agent(result_type=VideoAnalysis)

@agent.tool
async def video_analyzer_tool(video_url: str) -> AsyncGenerator[ProgressEvent, None]:
    """
    Herramienta para analizar un video y monitorear su progreso.
    """
    async for event in analyze_video(video_url):
        yield event

async def main():
    prompt = "Por favor, analiza el video en la URL 'https://example.com/my_video.mp4' y dame un resumen."

    print(f"Usuario: {prompt}\n")

    # Usar run_stream para manejar la respuesta y los eventos
    async with agent.run_stream(prompt) as result:
        # Monitoreo constante de la herramienta
        async for event in result.stream_events():
            if event.event == "on_tool_stream" and isinstance(event.data, ProgressEvent):
                progress = event.data
                print(f"🤖 Monitoreo: [{int(progress.percentage)}%] {progress.message}")

        # Respuesta final del modelo
        final_response = await result.get_final_response()
        print("\n✅ Tarea Finalizada. Respuesta del Modelo:")
        print(final_response)

if __name__ == "__main__":
    asyncio.run(main())