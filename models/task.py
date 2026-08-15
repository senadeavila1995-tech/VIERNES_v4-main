from dataclasses import dataclass, field


@dataclass
class Task:
    """
    Representa una tarea del plan.
    """

    action: str

    parameters: dict = field(default_factory=dict)

    description: str = ""

    order: int = 0

    def __str__(self):

        return f"{self.action} {self.parameters}"