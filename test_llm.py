from services.llm.llm_manager import LLMManager


llm = LLMManager()

respuesta = llm.ask(
    "¿Qué es FastAPI?"
)

print(respuesta)