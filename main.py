### Import section ###
# --- imports section --- #
from src.config import set_env_file

if __name__ == "__main__":
    set_env_file()





# from pydantic_ai import Agent
# from pydantic import BaseModel
# from pydantic import Field
# from pydantic_ai.providers.ollama import OllamaProvider
# from pydantic_ai.models.openai import OpenAIChatModel

# # Clase para definicion de respuesta de modelo
# class themeResponse(BaseModel):
#     city: str
#     country: str
#     description: str = Field(description="Include some interesting fact about that cicy...")

# def main(request: str):
#     try:
#         ollama_conn = OpenAIChatModel(
#             model_name = "qwen2.5:14b",
#             provider = OllamaProvider(
#                 base_url = "http://192.168.0.229:11434/v1"
#             )
#         )
#         print("Conexion realizada exitosamente")
#     except Exception as e:
#         print(f"Error durante la conexion. {e}")
#         return None

#     agent = Agent(ollama_conn, output_type = themeResponse)
#     result = agent.run_sync(request)
#     return result

# if __name__ == "__main__":
    # print(main("capital of coffe in the world"))
