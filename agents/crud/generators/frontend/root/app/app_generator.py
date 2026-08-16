from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class AppGenerator(BaseFrontendGenerator):

    name = "app"

    description = "Genera App.tsx del frontend."

    order = 140


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

        return '''import {
    BrowserRouter,
} from "react-router-dom";

import AppRoutes from "./routes";


export default function App() {

    return (
        <BrowserRouter>
            <AppRoutes />
        </BrowserRouter>
    );

}
'''


    def folder(self) -> str:
        return ""


    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return "App.tsx"
