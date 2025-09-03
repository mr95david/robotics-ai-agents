# Este modulo alberga la logica de la clase de eslabon, como el punto de interaccion directo del sistema de alto nivel con
# con los robots disponibles. Este se comunica de manera asilada y continua, dependiendo de inferencias con el manager del sistema;
# --- imports section --- #
from pydantic_ai import Agent
from pydantic_ai import Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.mcp import MCPServerSSE
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.mcp import MCPServerStreamableHTTP
# Self libraries
from src.services.model_factory import build_ollama_model
from src.models.system_prompts import ESLABON_PROMPT
from src.models.additional_structure import EslabonStatus
from src.models.additional_structure import TaskInfo
# Librerias para manejo de datos
from pydantic import AnyUrl
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import Literal
from typing import Optional
# Seccion de librerias de uso general
from httpx import AsyncClient
from asyncio import Lock

class Eslabon:

    __slots__ = (
        "_agent",
        "_name",
        "_prompt",
        "_model",
        "_mcp",
        "_eslabon_status",
        "_tasks",
        "_lock",
    )
    # _status = EslabonStatus.PENDING
    
    def __init__(
            self, 
            name: str,
            prompt: str | tuple = ESLABON_PROMPT,
            model: OpenAIChatModel = build_ollama_model()
        ) -> None:
        self._agent: Optional[Agent] = None
        self._name = name
        self._eslabon_status: EslabonStatus = EslabonStatus.UNASSIGNED
        self._lock: Lock = Lock()
        self._mcp = None
        self._model = model
        self._prompt = prompt
        self._tasks: Dict[str, TaskInfo] = dict()
        
        self.init_agent()
        print(f"Eslabon nombrado: {self._name}. Creado Correctamente.")

    # Designacion de agente de eslabon
    def init_agent(self) -> None:
        def get_current_status(include_prompt: bool) -> Dict[str, Any]:
            f"""Funcion para obtener el estado actual de ejecucion del eslabon {self._name} (Eslabon actual)"""
            return self.state(include_prompt=include_prompt)

        sync_tool = [
            Tool(get_current_status, takes_ctx=False, name="get_current_status")
        ]
        self._agent = Agent(
            model = self._model,
            tools = sync_tool,
            system_prompt = ESLABON_PROMPT
        )
        print("Asignacion de agente realizada")

    # Seccion de funciones de clase
    def assign_mcp(
        self,
        url: AnyStr | AnyUrl,
        type_connection: Literal["sse", "stdio", "stream"],
        *,
        args: Optional[list] = None, 
        allow_sampling: Optional[bool] = None,
        command: Optional[AnyStr] = None,
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[AsyncClient] = None,
        tool_prefix: Optional[AnyStr] = None
    ) -> None:
        if not url:
            raise ValueError("Parametro de url es obligatorio para la ejecucion")
        
        if type_connection == "sse":
            server = MCPServerSSE(
                url = url, headers = headers, 
                http_client = http_client,
                tool_prefix = tool_prefix,
                allow_sampling = allow_sampling
            )
        elif type_connection == "stdio":
            server = MCPServerStdio(
                command = command, args = args,
                tool_prefix = tool_prefix, allow_sampling = allow_sampling
            )
        elif type_connection == "stream":
            server = MCPServerStreamableHTTP(
                url = url, headers = headers, 
                http_client = http_client,
                tool_prefix = tool_prefix,
                allow_sampling = allow_sampling
            )
        else:
            raise ValueError("El parametro de 'type_connection' no concuerda con los valores validos intenta alguno de ['sse', 'stdio', 'stream']")
        self._eslabon_status = EslabonStatus.AVAILABLE 
        self._mcp = server

    def state(self, *, include_prompt: bool = False) -> Dict[str, Any]:
        """
        Retorna un snapshot del estado actual. Por defecto oculta el prompt principal.
        """
        data: Dict[str, Any] = {
            "name": self._name,
            "status": self._eslabon_status.value if hasattr(self._eslabon_status, "value") else self._eslabon_status,
            "tasks_pending": list(self._tasks),
            "mcp_assigned": self._mcp is not None,
        }
        if include_prompt:
            data["system_prompt"] = self._prompt
        return data
    
    # Tareas disponibles relacionadas al modelo de lenguaje
