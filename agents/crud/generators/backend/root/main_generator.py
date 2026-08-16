from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.naming_resolver import NamingResolver


class MainGenerator(BaseGenerator):
    """
    Genera el punto de entrada FastAPI.

    El orden de inicialización es deliberadamente:

        1. Importar DTO Response.
        2. Reconstruir todos los modelos Pydantic.
        3. Importar los routers.
        4. Crear la aplicación FastAPI.
        5. Registrar los routers.

    Esto evita que FastAPI procese los response_model
    antes de que Pydantic haya resuelto los forward references.
    """

    name = "main"

    description = "Genera la aplicación FastAPI principal."

    order = 140

    def generate(
        self,
        context: GenerationContext,
    ):

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
            getattr(
                context,
                "definition",
                None,
            )
        )

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        router_imports = []

        routers = []

        response_imports = []

        response_models = []

        for definition in context.definitions.values():

            module = self.snake_name_from_definition(
                definition
            )

            entity = module

            response_class = NamingResolver.class_name(
                definition.entity,
                "dto_response",
            )

            # ==================================
            # DTO Response
            # ==================================

            response_imports.append(
                f"from backend.modules.{module}.dto."
                f"{module}_response import "
                f"{response_class}"
            )

            response_models.append(
                response_class
            )

            # ==================================
            # Router
            # ==================================

            router_imports.append(
                f"from backend.modules.{module}.routes."
                f"{module}_route import router as "
                f"{entity}_router"
            )

            routers.append(
                f"app.include_router({entity}_router)"
            )

        # ==================================
        # Imports DTO Response
        # ==================================

        response_imports_text = ""

        if response_imports:

            response_imports_text = (
                "\n"
                + "\n".join(
                    sorted(
                        set(response_imports)
                    )
                )
            )

        # ==================================
        # Rebuild Pydantic
        # ==================================

        response_rebuild = ""

        if response_models:

            namespace_lines = []

            for response_class in sorted(
                set(response_models)
            ):

                namespace_lines.append(
                    f'    "{response_class}": '
                    f"{response_class},"
                )

            response_rebuild = f'''

_RESPONSE_MODELS = {{
{chr(10).join(namespace_lines)}
}}


for _model in _RESPONSE_MODELS.values():

    _model.model_rebuild(
        force=True,
        _types_namespace=_RESPONSE_MODELS,
    )
'''

        # ==================================
        # Imports Router
        # ==================================

        router_imports_text = ""

        if router_imports:

            router_imports_text = (
                "\n"
                + "\n".join(
                    sorted(
                        set(router_imports)
                    )
                )
            )

        # ==================================
        # Generated main.py
        # ==================================

        return f'''from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.framework.database.init_database import init_database
from backend.framework.exceptions.database import DatabaseIntegrityError
{response_imports_text}
{response_rebuild}
{router_imports_text}


app = FastAPI(
    title="VIERNES Generated API"
)


@app.on_event("startup")
def startup():

    init_database()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DatabaseIntegrityError)
async def database_integrity_exception_handler(
    request,
    exc: DatabaseIntegrityError,
):
    return JSONResponse(
        status_code=409,
        content={{
            "detail": exc.message,
        }},
    )


{chr(10).join(routers)}
'''

    def folder(self):

        return ""

    def filename(
        self,
        context: GenerationContext,
    ):

        return "main.py"

    def snake_name_from_definition(
        self,
        definition,
    ):

        return NamingResolver.snake(
            definition.entity
        )
