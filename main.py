### Import section ###
# --- imports section --- #
# General dependencies
import asyncio
from typing import AsyncGenerator, Literal
from src.services.model_factory import build_ollama_model
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import Callable, Awaitable
# from pydantic_ai.tool import tool

# --------------------------------------------------------------------------
## 1. Definición de los modelos Pydantic
# --------------------------------------------------------------------------
class ProgressEvent(BaseModel):
    """Modelo para los eventos de progreso emitidos por la herramienta."""
    message: str = Field(..., description="Mensaje descriptivo del progreso.")
    percentage: float = Field(..., description="Porcentaje de completitud de la tarea.")

class VideoAnalysis(BaseModel):
    """Modelo para el resultado final y estructurado del análisis del video."""
    summary: str = Field(..., description="Un resumen conciso del contenido del video.")
    key_topics: list[str] = Field(..., description="Una lista de los temas principales mencionados en el video.")

class ToolCompletionReport(BaseModel):
    """Modelo para el resultado final de la herramienta que se devuelve al LLM."""
    status: str = Field(..., description="Estado final de la ejecución de la herramienta.")
    message: str = Field(..., description="Mensaje de confirmación para el LLM.")

ProgressCallback = Callable[[ProgressEvent], Awaitable[None]]
# --------------------------------------------------------------------------
## 2. Herramienta Asíncrona que emite eventos de progreso
# --------------------------------------------------------------------------

async def _internal_video_processor(
    video_url: str,
    callback: ProgressCallback,
):
    """
    Procesador interno que ahora invoca un callback para reportar progreso
    en lugar de usar 'yield'.
    """
    print(f"⚙️ Iniciando el análisis del video: {video_url}")

    await callback(ProgressEvent(message="Iniciando descarga del video...", percentage=10.0))
    await asyncio.sleep(2)

    await callback(ProgressEvent(message="Extrayendo audio y transcribiendo...", percentage=50.0))
    await asyncio.sleep(3)

    await callback(ProgressEvent(message="Análisis de contenido finalizado, generando resumen...", percentage=90.0))
    await asyncio.sleep(2)

    await callback(ProgressEvent(message="Análisis completado exitosamente.", percentage=100.0))

# El decorador @tool expone la función al agente de IA



# --------------------------------------------------------------------------
## 3. Configuración y Ejecución del Agente
# --------------------------------------------------------------------------


async def main():
    """Función principal que ahora define el callback y la herramienta."""

    # 1. Define la función de callback que imprimirá el progreso en la consola.
    async def progress_callback(event: ProgressEvent):
        print(f"🤖 Monitoreo: [{int(event.percentage)}%] {event.message}")

    # 2. Define la herramienta que el LLM puede invocar.
    #    Esta herramienta ahora conoce y utiliza el 'progress_callback'.
    async def video_analyzer_tool(video_url: str) -> ToolCompletionReport:
        """
        Herramienta para analizar un video. Reporta su progreso de forma asíncrona
        y devuelve un reporte de finalización al ser completada.
        """
        await _internal_video_processor(video_url, callback=progress_callback)
        
        # 3. Devuelve un objeto simple y serializable para informar al LLM que la tarea terminó.
        return ToolCompletionReport(
            status="completed",
            message="El video ha sido procesado exitosamente. Ahora puedes generar el resumen final."
        )
    model = build_ollama_model()
    # Configura el agente con la herramienta y el tipo de resultado esperado
    agent = Agent(
        model,
        tools=[video_analyzer_tool],
        output_type=VideoAnalysis
    )

    prompt = "Por favor, analiza el video en 'https://example.com/my_video.mp4' y dame un resumen con sus temas clave."

    print(f"🧑 Usuario: {prompt}\n")

    # 4. Ejecuta el agente. Ya no se necesita el bucle 'stream_events'.
    #    El callback se encargará del monitoreo.
    final_response = await agent.run(prompt)
    
    print("\n✅ ¡Tarea completada! Obteniendo respuesta final del modelo...")
    print("\n📝 Respuesta Final Estructurada:")
    print(final_response)
    
if __name__ == "__main__":
    # Asegúrate de configurar tu clave de API de OpenAI como variable de entorno
    # (ej. OPENAI_API_KEY) o el proveedor de LLM que uses.
    asyncio.run(main())

# async def main():
#     """Función principal para ejecutar el agente."""
#     model = build_ollama_model()
#     # Configura el agente con la herramienta y el tipo de resultado esperado
#     agent = Agent(
#         model,
#         tools=[video_analyzer_tool],
#         output_type=VideoAnalysis
#     )

#     prompt = "Por favor, analiza el video en 'https://example.com/my_video.mp4' y dame un resumen con sus temas clave."

#     print(f"🧑 Usuario: {prompt}\n")

#     # agent.run_stream() permite procesar la respuesta y los eventos en tiempo real
#     async with agent.run_stream(prompt) as result:
#         # Bucle para monitorear los eventos de la herramienta
#         async for event in result.stream_events():
#             # Filtramos solo los eventos de streaming de nuestra herramienta
#             if event.event == "on_tool_stream" and isinstance(event.data, ProgressEvent):
#                 progress = event.data
#                 print(f"🤖 Monitoreo: [{int(progress.percentage)}%] {progress.message}")

#         # Una vez que la herramienta termina, el LLM genera la respuesta final
#         print("\n✅ ¡Tarea completada! Obteniendo respuesta final del modelo...")
#         final_response = await result.get_final_response()
        
#         print("\n📝 Respuesta Final Estructurada:")
#         print(final_response)

# if __name__ == "__main__":
#     # Asegúrate de configurar tu clave de API de OpenAI (o el LLM que uses)
#     # como una variable de entorno, por ejemplo: OPENAI_API_KEY
#     # import os
#     # os.environ["OPENAI_API_KEY"] = "sk-..."
    
#     asyncio.run(main())
# import asyncio
# from pydantic_ai import Agent
# # Self package modules
# from src.services.model_factory import build_ollama_model
# from src.models.output_models import SimpleResponse
# from src.models.system_prompts import SECOND_SYSTEM_PROMPT
# from pydantic_ai.mcp import MCPServerSSE

# # if __name__ == "__main__":
# mcp_server = MCPServerSSE(url = 'https://mcp.api.coingecko.com/sse')

# model = build_ollama_model()
# agent = Agent(
#     model,
#     output_type = SimpleResponse,
#     system_prompt = (SECOND_SYSTEM_PROMPT),
#     toolsets=[mcp_server],
#     # mcp_servers=[mcp_server]
# )
# async def test_():
#     async with agent:
#         temp_response = await agent.run(user_prompt=(
#         "Consulta las plataformas de assets (CoinGecko MCP). "
#         "Devuélveme un resumen, cuantos items hay y muéstrame 5 IDs y nombres. "
#         "Usa jq_filter para pedir solo 'id,name' y limitar a 5."
#     ))
#     print(temp_response)

# if __name__ == "__main__":
#     asyncio.run(test_())


