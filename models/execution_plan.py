from dataclasses import dataclass, field


@dataclass
class ExecutionPlan:

    steps: list[str] = field(default_factory=list)

    questions: list[str] = field(default_factory=list)

    confidence: float = 1.0

    requires_confirmation: bool = False