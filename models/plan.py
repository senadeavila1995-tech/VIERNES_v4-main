from dataclasses import dataclass, field

from models.task import Task


@dataclass
class Plan:
    """
    Representa un conjunto de tareas que Viernes debe ejecutar.
    """

    steps: list[Task] = field(default_factory=list)


    def add(
        self,
        action: str,
        parameters: dict = None,
        description: str = ""
    ):
        """
        Agrega una nueva tarea al plan.
        """

        if parameters is None:
            parameters = {}


        task = Task(
            action=action,
            parameters=parameters,
            description=description,
            order=len(self.steps) + 1
        )


        self.steps.append(task)


    def get_next_task(self):
        """
        Obtiene la siguiente tarea pendiente.
        """

        if not self.steps:
            return None

        return self.steps[0]


    def is_empty(self):
        """
        Verifica si el plan no tiene tareas.
        """

        return len(self.steps) == 0


    def __str__(self):

        result = "Plan:\n"

        for task in self.steps:
            result += (
                f"{task.order}. "
                f"{task.action} - "
                f"{task.parameters}\n"
            )

        return result