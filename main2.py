### Import section ###
from pydantic_ai import Agent
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIChatModel

ollama_conn = OpenAIChatModel(
    model_name = "qwen2.5:14b",
    provider = OllamaProvider(
        base_url = "http://192.168.0.229:11434/v1"
    )
)

agent = Agent(ollama_conn)

