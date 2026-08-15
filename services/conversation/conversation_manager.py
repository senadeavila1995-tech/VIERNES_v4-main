from agents.memory_agent import MemoryAgent
from models.action_result import ActionResult


class ConversationManager:

    def __init__(self):

        self.memory = MemoryAgent()

        self.state = None

        self.pending_action = None

        self.pending_data = {}

    # ============================================
    # Estado
    # ============================================

    def start(self, action, **data):

        self.state = "waiting"

        self.pending_action = action

        self.pending_data = data

    def clear(self):

        self.state = None

        self.pending_action = None

        self.pending_data = {}

    def is_waiting(self):

        return self.state == "waiting"

    # ============================================
    # Procesar respuesta
    # ============================================

    def handle(self, text):

        if not self.is_waiting():

            return None

        action = self.pending_action

        if action == "overwrite_document":

            answer = text.lower().strip()

            if answer in [
                "si",
                "sí",
                "s",
                "yes",
                "y"
            ]:

                result = ActionResult(
                    success=True,
                    message="El documento puede sobrescribirse."
                )

            else:

                result = ActionResult(
                    success=False,
                    message="Operación cancelada."
                )

            self.clear()

            return result

        return None