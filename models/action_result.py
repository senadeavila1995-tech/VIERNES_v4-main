from dataclasses import dataclass, field
from typing import Any


@dataclass
class ActionResult:
    success: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    next_question: str | None = None