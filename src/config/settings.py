# --- imports section --- #
# Data control vars
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
# Typing data control
from typing import Any
from typing import AnyStr
from pydantic import AnyUrl
from pydantic import Field

# TODO: Mejorar sistema de generalizacion de informacion - incluyendo validacion de obtencion de datos

class OllamaSettings(BaseSettings):
    # Main Ollama Configurations 
    ollama_url: AnyUrl = Field(..., alias = "OLLAMA_URL")
    ollama_port: int = Field(..., alias = "OLLAMA_PORT")
    ollama_key: Any = Field(..., alias = "OLLAMA_KEY")    

class ModelSettings(BaseSettings):
    # Main Model Configuration
    # --- General tool model --- #
    tool_model: str = Field(..., alias="GENERAL_MODEL")

    tool_model_temp: float = Field(..., alias="LLM_TEMPERATURE", ge=0, le=2)
    tool_model_cntx: int = Field(..., alias="LLM_MAX_TOKENS", gt=0)
    tool_model_timeout: float = Field(..., alias="LLM_TIME_OUT", gt=0)

    # --- General vision model --- #
    vision_model: AnyStr = Field(..., alias="VISUAL_GENERAL_MODEL")

    # --- General Thinking model --- #
    thinking_model: AnyStr = Field(..., alias="THINKING_GENERAL_MODEL")

    # --- General Thinking model --- #
    embedding_model: AnyStr = Field(..., alias="EMBEDDING_GENERAL_MODEL")

class Settings(BaseSettings):
    # General settings assignation
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    ollama: OllamaSettings = OllamaSettings()
    model: ModelSettings = ModelSettings()

# Input Settings from env
settings: Settings = Settings()