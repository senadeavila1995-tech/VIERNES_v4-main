from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)
from agents.crud.models.generation_context import GenerationContext


class TableGenerator(BaseFrontendGenerator):

    name = "frontend_table"

    description = "Genera la tabla React."

    order = 80

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        component = self.component_name(context)

        headers = []
        cells = []

        for field in context.fields:

            headers.append(f"<th>{field.name}</th>")

            cells.append(f"<td>{{item.{field.name}}}</td>")

        headers = "\n".join(headers)

        cells = "\n".join(cells)

        return f"""

interface Props {{

    data:any[];

}}

export default function {component}Table({{data}}:Props) {{

    return (

        <table className="table table-striped">

            <thead>

                <tr>

{headers}

                </tr>

            </thead>

            <tbody>

                {{data.map((item:any)=>(

                    <tr key={{item.id}}>

{cells}

                    </tr>

                ))}}

            </tbody>

        </table>

    );

}}
"""
