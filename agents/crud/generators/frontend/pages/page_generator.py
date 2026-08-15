from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class PageGenerator(BaseFrontendGenerator):
    """
    Genera páginas React CRUD.

    La página actúa como contenedor principal del módulo:

    - Consume el hook CRUD.
    - Carga los registros.
    - Pasa los registros a la tabla.
    - Abre/cierra el modal.
    - Coordina el formulario con la recarga de datos.
    """

    name = "page"

    description = "Genera páginas frontend React."

    order = 100

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        component = self.page_name(context)

        table = self.table_name(context)

        form = self.form_name(context)

        modal = self.modal_name(context)

        module = self.snake_name(context)

        hook = self.hook_name(context)

        variable = self.camel_name(context)

        return f'''import {{ useState }} from "react";

import {{ {hook} }} from "../hooks/{hook}";

import {table} from "../components/{module}Table";

import {form} from "../components/{module}Form";

import {modal} from "../components/{module}Modal";


export default function {component}() {{

    const {{
        {variable},
        loading,
        error,
        load,
    }} = {hook}();

    const [open, setOpen] = useState(false);


    return (

        <div className="container mt-4">

            <div className="d-flex justify-content-between align-items-center mb-3">

                <h2>
                    {context.entity_name}
                </h2>

                <button
                    type="button"
                    className="btn btn-primary"
                    onClick={{() => setOpen(true)}}
                >
                    Nuevo
                </button>

            </div>


            {{error && (
                <div className="alert alert-danger">
                    {{error}}
                </div>
            )}}


            <{modal}
                open={{open}}
                onClose={{() => setOpen(false)}}
            >

                <{form}
                    onSaved={{async () => {{
                        await load();
                        setOpen(false);
                    }}}}
                />

            </{modal}>


            {{loading ? (

                <div className="text-center py-4">
                    Cargando...
                </div>

            ) : (

                <{table}
                    data={{{variable}}}
                />

            )}}

        </div>

    );

}}
'''

