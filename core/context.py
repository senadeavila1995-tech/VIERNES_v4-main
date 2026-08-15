from dataclasses import dataclass, field


@dataclass
class Context:

    # =====================================================
    # Proyecto
    # =====================================================

    current_project: str | None = None

    project_path: str | None = None

    language: str | None = None

    framework: str | None = None

    frontend: str | None = None

    database: str | None = None


    # =====================================================
    # Documento
    # =====================================================

    current_document: str | None = None

    opened_files: list[str] = field(
        default_factory=list
    )


    # =====================================================
    # IA
    # =====================================================

    provider: str = "openai"


    # =====================================================
    # Task / Planner
    # =====================================================

    # Última acción ejecutada por VIERNES
    #
    # Ejemplo:
    # create_project
    # write_document
    # run_terminal

    last_action: str | None = None


    # =====================================================
    # Scanner
    # =====================================================

    scanned: bool = False

    project_index: dict = field(
        default_factory=dict
    )