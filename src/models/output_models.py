# --- imports section --- #
# pydantic principal data management 
from pydantic import BaseModel
from pydantic import Field
# Libraries for typing configurate
from typing import Literal

class SimpleResponse(BaseModel):
    text_output: str = Field(..., description = "Text response for user request...")


