from agents.crud.crud_generator import CrudGenerator
from agents.crud.models.generation_context import GenerationContext


class CrudAgent:
    """
    Fachada de alto nivel para la generación CRUD.

    La lógica real de generación pertenece a CrudGenerator.

    Flujo:

        Router
          ↓
        CrudAgent
          ↓
        CrudGenerator
          ↓
        RelationshipResolver
          ↓
        GeneratorRegistry
          ↓
        Generators
          ↓
        FileWriter
    """

    def __init__(self):

        self.generator = CrudGenerator()

    # ==========================================================
    # Ejecución
    # ==========================================================

    def execute(
        self,
        context: GenerationContext,
    ):

        # ======================================================
        # Delegar generación al motor real
        # ======================================================

        paths = self.generator.generate(
            context
        )

        # ======================================================
        # Resultado normalizado
        # ======================================================

        return {
            "success": not context.has_errors,
            "entity": context.entity_name,
            "database": context.project.database,
            "generated_files": context.generated_files,
            "warnings": context.warnings,
            "errors": context.errors,
            "results": [
                {
                    "file": str(path),
                    "success": True,
                }
                for path in paths
            ],
        }
