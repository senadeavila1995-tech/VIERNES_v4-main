from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)
from agents.crud.models.generation_context import GenerationContext


class ToolbarGenerator(BaseFrontendGenerator):
    """
    Genera la barra de acciones del módulo CRUD.
    """

    name = "frontend_toolbar"

    description = "Genera barra de acciones React."

    order = 95

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        component = f"{self.pascal_name(context)}Toolbar"

        return f'''

interface Props {{
    onCreate: () => void;
}}

export default function {component}({{ onCreate }}: Props) {{
    return (
        <div className="d-flex justify-content-between align-items-center mb-3">
            <div>
                <h5 className="mb-0">
                    {context.entity_name}
                </h5>
            </div>

            <button
                type="button"
                className="btn btn-primary"
                onClick={{onCreate}}
            >
                Nuevo
            </button>
        </div>
    );
}}
'''

    def folder(self) -> str:
        return "components"

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.snake_name(context)}Toolbar.tsx"
