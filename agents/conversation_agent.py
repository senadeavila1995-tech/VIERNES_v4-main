from agents.llm_agent import LLMAgent
from agents.memory_agent import MemoryAgent


class ConversationAgent:
    """
    Maneja la conversación básica de VIERNES.

    No crea Intent.
    No ejecuta tareas.
    No crea planes.

    Solo procesa conversaciones simples.
    """

    def __init__(self):

        self.memory = MemoryAgent()

        self.llm = LLMAgent()


    # =====================================================
    # CHAT
    # =====================================================

    def chat(self, text):

        return self.llm.chat(text)


    # =====================================================
    # RESPUESTA DIRECTA
    # =====================================================

    def answer(self, text):

        return self.llm.chat(text)


    # =====================================================
    # COMPATIBILIDAD
    # =====================================================

    def detect(self, text):

        """
        Mantiene compatibilidad temporal.

        Ya no devuelve Intent.
        Devuelve el texto para PlannerAgent.
        """

        return text