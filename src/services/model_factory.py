# dependencies imports section
from src.config import settings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
# Importe de librerias para procesamiento de tipado
from typing import Any
from typing import Dict
from typing import Optional


# Princial function for openai/ollama model 
def build_ollama_model(
        *,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[float] = None,
        request_timeout: Optional[float] = None
        ) -> OpenAIChatModel:
    
    try:
        llm_cfg = settings.model
        ollama_cfg = settings.ollama
    except Exception as e:
        raise ValueError("El objeto de settings no está configurado correctamente.") from e
        
    base_settings: Dict[str, Any] = {
        "temperature": llm_cfg.tool_model_temp if temperature is None else temperature,
        "max_tokens": llm_cfg.tool_model_cntx if max_tokens is None else max_tokens,
        "timeout": llm_cfg.tool_model_timeout if request_timeout is None else request_timeout,
    }

    base_url = str(ollama_cfg.ollama_url)[:-1] + ':' + str(ollama_cfg.ollama_port) + '/'
    model_name = llm_cfg.tool_model if model_name is None else model_name
    # print(base_url)
    provider: OllamaProvider = OllamaProvider(
        base_url = base_url + 'v1'
    )
    
    return OpenAIChatModel(
        model_name = model_name,
        provider = provider,
        settings = base_settings
    )