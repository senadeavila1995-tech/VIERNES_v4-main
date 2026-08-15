from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class RootRouteGenerator(BaseFrontendGenerator):
    """
    Genera las rutas raíz de la aplicación React.

    Reúne las rutas de todos los módulos CRUD generados.
    """

    name = "root_routes"

    description = "Genera el router raíz del frontend."

    order = 130

    def generate(
        self,
        context: GenerationContext,
    ):
        """
        Genera un archivo perteneciente a la raíz
        del frontend, no a un módulo CRUD.
        """

        if not self.validate(context):
            raise ValueError(
                f"El generador '{self.name}' no puede ejecutarse."
            )

        return self.build_file(
            entity="",
            folder=self.folder(),
            filename=self.filename(context),
            content=self.generate_content(context),
            description=self.description,
        )

    def validate(
        self,
        context: GenerationContext,
    ) -> bool:

        return bool(
            getattr(context, "definitions", None)
        )

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        definitions = getattr(
            context,
            "definitions",
            {},
        )

        imports = []
        routes = []

        for definition in definitions.values():

            module = self.snake_name_from_definition(
                definition
            )

            page = self.pascal_name_from_definition(
                definition
            ) + "Page"

            imports.append(
                f'import {page} from "./modules/{module}/pages/{page}";'
            )

            routes.append(
                f'''    {{
        path: "/{module}",
        element: <{page} />,
    }},'''
            )

        return f'''import {{
    BrowserRouter,
    Link,
    Route,
    Routes,
}} from "react-router-dom";

{chr(10).join(imports)}


function Inicio() {{

    return (

        <div className="container mt-4">

            <h1>
                VIERNES CRUD
            </h1>

            <p>
                Seleccione un módulo:
            </p>

            <div className="d-flex gap-2 flex-wrap">

{chr(10).join(
    f'''                <Link
                    to="/{self.snake_name_from_definition(definition)}"
                    className="btn btn-primary"
                >
                    {definition.entity}
                </Link>'''
    for definition in definitions.values()
)}

            </div>

        </div>

    );

}}


export default function App() {{

    return (

        <BrowserRouter>

            <nav className="navbar navbar-dark bg-dark">

                <div className="container">

                    <Link
                        to="/"
                        className="navbar-brand"
                    >
                        VIERNES CRUD
                    </Link>

                    <div className="d-flex gap-2">

{chr(10).join(
    f'''                        <Link
                            to="/{self.snake_name_from_definition(definition)}"
                            className="btn btn-outline-light btn-sm"
                        >
                            {definition.entity}
                        </Link>'''
    for definition in definitions.values()
)}

                    </div>

                </div>

            </nav>

            <Routes>

                <Route
                    path="/"
                    element={{<Inicio />}}
                />

{chr(10).join(
    f'''                <Route
                    path="/{self.snake_name_from_definition(definition)}"
                    element={{<{self.pascal_name_from_definition(definition)}Page />}}
                />'''
    for definition in definitions.values()
)}

            </Routes>

        </BrowserRouter>

    );

}}
'''

    def folder(self) -> str:

        return ""

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return "App.tsx"

    # ==========================================================
    # Helpers para CrudDefinition
    # ==========================================================

    def snake_name_from_definition(
        self,
        definition,
    ) -> str:

        from agents.crud.resolvers.naming_resolver import NamingResolver

        return NamingResolver.snake(
            definition.entity
        )

    def pascal_name_from_definition(
        self,
        definition,
    ) -> str:

        from agents.crud.resolvers.naming_resolver import NamingResolver

        return NamingResolver.pascal(
            definition.entity
        )
