from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)
from agents.crud.models.generation_context import GenerationContext


class FilterGenerator(BaseFrontendGenerator):
    """
    Genera el componente React de filtros del módulo CRUD.
    """

    name = "frontend_filter"

    description = "Genera filtros React."

    order = 96

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        component = f"{self.pascal_name(context)}FilterComponent"

        inputs = []

        for field in context.fields:

            inputs.append(
                f'''            <div className="col-md-3">
                <label className="form-label">
                    {field.name}
                </label>

                <input
                    type="text"
                    className="form-control"
                    name="{field.name}"
                />
            </div>'''
            )

        body = "\n\n".join(inputs)

        return f'''interface Props {{
    onFilter?: (filters: Record<string, unknown>) => void;
}}

export default function {component}({{ onFilter }}: Props) {{
    return (
        <div className="row g-3 mb-3">
{body}

            <div className="col-md-3 d-flex align-items-end">
                <button
                    type="button"
                    className="btn btn-outline-primary"
                    onClick={{() => onFilter?.({{}})}}
                >
                    Filtrar
                </button>
            </div>
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

        return f"{self.snake_name(context)}Filter.tsx"
