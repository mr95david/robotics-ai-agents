"""
Modulo para control de configuracion principal de agentes

Este modulo maneja las configuraciones para la creacion de agentes segun las necesidades estipuladas,
asi mismo se espera que se incluyan las configuraiones adicionales, mcp, a2a y demas necesarias.
"""

from .settings import OllamaSettings
from .settings import ModelSettings
from .settings import Settings


__all__ = [
    'OllamaSettings',
    'ModelSettings',
    'Settings'
]