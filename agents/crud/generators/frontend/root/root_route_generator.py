from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class RootRouteGenerator(BaseFrontendGenerator):

    name = "root_routes"

    description = "Genera el router raíz del frontend."

    order = 130


    def generate(
        self,
        context: GenerationContext,
    ):

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

            route_name = self.camel_name_from_definition(
                definition
            )

            imports.append(
                f'import {{ {route_name}Routes }} from "./modules/{module}/routes";'
            )

            routes.append(
                f"    ...{route_name}Routes,"
            )

        return (
            "import {\n"
            "    Routes,\n"
            "    Route,\n"
            "} from \"react-router-dom\";\n\n"
            "import HomePage from \"./HomePage\";\n\n"
            +
            "\n".join(imports)
            +
            "\n\n\nconst routes = [\n"
            "    {\n"
            "        path: \"/\",\n"
            "        element: <HomePage />,\n"
            "    },\n"
            +
            "\n".join(routes)
            +
            "\n];\n\n"
            +
            "export default function AppRoutes() {\n\n"
            "    return (\n"
            "        <Routes>\n"
            "            {routes.map((route) => (\n"
            "                <Route\n"
            "                    key={route.path}\n"
            "                    {...route}\n"
            "                />\n"
            "            ))}\n"
            "        </Routes>\n"
            "    );\n\n"
            "}\n"
        )


    def folder(self) -> str:

        return ""


    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return "routes.tsx"


    def snake_name_from_definition(
        self,
        definition,
    ) -> str:

        from agents.crud.resolvers.naming_resolver import NamingResolver

        return NamingResolver.snake(
            definition.entity
        )


    def camel_name_from_definition(
        self,
        definition,
    ) -> str:

        from agents.crud.resolvers.naming_resolver import NamingResolver

        return NamingResolver.camel(
            definition.entity
        )
