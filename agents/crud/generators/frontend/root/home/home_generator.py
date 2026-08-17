from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class HomeGenerator(BaseFrontendGenerator):

    name = "home"

    description = "Genera la página principal del frontend."

    order = 125

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

        return '''export default function HomePage() {

    return (

        <div className="container mt-4">

            <div className="text-center py-5">

                <h1 className="mb-3">
                    Bienvenido
                </h1>

                <p className="text-muted">
                    Aplicación generada automáticamente por VIERNES.
                </p>

            </div>

        </div>

    );

}
'''

    def folder(self) -> str:

        return ""

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return "HomePage.tsx"
