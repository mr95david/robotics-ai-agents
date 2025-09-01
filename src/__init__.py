"""
Sistema de comunicacion con modelos de lenguaje - test avanzado para la correcta configuracion de dichos paquetes

Este paquete involucra la estructura proxima para el desarrollo de aplicaciones que permitan la exploracion de propuestas academicas,
relacionadas a ''decision-making process in robotics'' o ''emboided ai'', a partir de esta estructura se busca generalizar las estructuras derivadas,
que puedan funcionar en los diferentes proyectos.
"""


# --- Informacion del paquete --- #
__version__     = "0.1.0"
__author__      = "Elio David Triana Rodriguez"
__email__       = "eliotrianar95@gmail.com"

# --- Lista de simbolos publicos --- #
# En esta seccion se agregan los paquetes de uso publicos relacionados al programa desarrollado.
all = [
    # Incluir paquete del modudo desarrolado
    '__version__',   
]

# --- Seccion de configuracion de logger para paquete --- #
## NOTA: Considerando el uso del paquete de pydantic seria importante definir cuales estrategias de debug crear ## 
# Tal vez -- import logfire
import logging