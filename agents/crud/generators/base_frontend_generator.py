from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext


class BaseFrontendGenerator(BaseGenerator):
    """
    Clase base para todos los generadores React + TypeScript.

    Todos los generadores del frontend heredan de aquí.

    Se encarga de:

    - Definir la capa frontend.
    - Helpers de nombres.
    - Helpers de TypeScript.
    - Helpers de React.
    """

    # ==========================================================
    # CAPA
    # ==========================================================

    def layer(self):

        return "frontend"

    # ==========================================================
    # NOMBRES
    # ==========================================================

    def component_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.pascal_name(context)

    def page_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.pascal_name(context)}Page"

    def table_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.pascal_name(context)}Table"

    def form_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.pascal_name(context)}Form"

    def modal_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.pascal_name(context)}Modal"

    def toolbar_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.pascal_name(context)}Toolbar"

    def filter_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.pascal_name(context)}Filters"

    def hook_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"use{self.pascal_name(context)}"

    def api_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.camel_name(context)}Api"

    def service_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.camel_name(context)}Service"

    def type_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.pascal_name(context)

    def route_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.snake_name(context)}.routes"

    def module_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.snake_name(context)

    # ==========================================================
    # TYPESCRIPT
    # ==========================================================

    def ts_type(self, field) -> str:

        mapper = {
            "string": "string",
            "text": "string",
            "integer": "number",
            "int": "number",
            "bigint": "number",
            "float": "number",
            "double": "number",
            "decimal": "number",
            "boolean": "boolean",
            "bool": "boolean",
            "date": "string",
            "datetime": "string",
            "time": "string",
            "uuid": "string",
        }

        return mapper.get(
            field.type.lower(),
            "any",
        )

    # ==========================================================
    # REACT
    # ==========================================================

    def react_imports(self):

        return (
            "import React from 'react';\n"
            "import { useEffect, useState } from 'react';"
        )

    def bootstrap_imports(self):

        return "import 'bootstrap/dist/css/bootstrap.min.css';"

    def axios_import(self):

        return "import axios from 'axios';"

    # ==========================================================
    # HELPERS
    # ==========================================================

    def interface_fields(
        self,
        context: GenerationContext,
    ) -> str:

        lines = []

        for field in context.fields:

            lines.append(f"    {field.name}: {self.ts_type(field)};")

        return "\n".join(lines)

    def default_values(
        self,
        context: GenerationContext,
    ) -> str:

        values = []

        for field in context.fields:

            ts = self.ts_type(field)

            if ts == "number":

                value = "0"

            elif ts == "boolean":

                value = "false"

            else:

                value = "''"

            values.append(f"    {field.name}: {value},")

        return "\n".join(values)
