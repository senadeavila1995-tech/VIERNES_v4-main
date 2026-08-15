from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class TableGenerator(BaseFrontendGenerator):
    """
    Genera tablas React + TypeScript para listar registros.
    """

    name = "frontend_table"

    description = "Genera componente tabla React."

    order = 80

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        component = self.table_name(context)

        headers = []
        rows = []

        for field in context.fields:

            headers.append(f"<th>{field.name}</th>")

            rows.append(f"<td>{{item.{field.name}}}</td>")

        headers_html = "\n".join(headers)
        rows_html = "\n".join(rows)

        return f"""
import React from "react";


interface Props {{

    data: any[];

}}


export default function {component}({{data}}: Props){{


    return (

        <table className="table table-striped">

            <thead>

                <tr>

                    {headers_html}

                </tr>

            </thead>


            <tbody>

                {{data.map((item:any)=>(

                    <tr key={{item.id}}>

                        {rows_html}

                    </tr>

                ))}}

            </tbody>


        </table>

    );

}}
"""
