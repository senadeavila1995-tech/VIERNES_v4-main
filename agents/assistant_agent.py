from agents.conversation_agent import ConversationAgent
from agents.memory_agent import MemoryAgent
from agents.planner_agent import PlannerAgent

from core.executor import Executor
from core.router import Router

from services.conversation.conversation_manager import ConversationManager

from models.action_result import ActionResult


class AssistantAgent:
    """
    Agente principal de VIERNES.

    Flujo:

    Usuario
        ↓
    ConversationAgent
        ↓
    PlannerAgent
        ↓
    Plan
        ↓
    Executor
        ↓
    Router
        ↓
    Agents
    """

    def __init__(self):

        self.conversation = ConversationAgent()

        self.memory = MemoryAgent()

        self.planner = PlannerAgent()

        self.router = Router()

        self.task_manager = Executor()

        self.conversation_manager = ConversationManager()


    def process(self, text: str):

        pending = self.conversation_manager.handle(text)

        if pending is not None:
            return pending.message


        # ==========================================
        # 1. Preparar solicitud del usuario
        # ==========================================

        request = self.conversation.detect(text)


        # ==========================================
        # 2. Crear Plan
        # ==========================================

        plan = self.planner.build_plan(request)


        # ==========================================
        # 3. Guardar última acción
        # ==========================================

        if plan.steps:

            self.memory.update_last_action(
                plan.steps[0].action
            )


        # ==========================================
        # 4. Mostrar Plan
        # ==========================================

        print("\n📋 Plan de ejecución\n")


        for index, step in enumerate(plan.steps, start=1):

            print(
                f"{index}. {step}"
            )


        # ==========================================
        # 5. Ejecutar Plan
        # ==========================================

        result = self.task_manager.execute(
            self.router,
            plan
        )


        # ==========================================
        # 6. Respuesta
        # ==========================================

        if isinstance(result, ActionResult):

            if result.data:

                # Caso lista de proyectos
                if isinstance(result.data, list):

                    first = result.data[0]

                    if "projects" in first:

                        projects = first["projects"]

                        text = "📁 Proyectos disponibles:\n\n"

                        for project in projects:

                            text += f"• {project}\n"

                        return text


                return result.data

        return result.message