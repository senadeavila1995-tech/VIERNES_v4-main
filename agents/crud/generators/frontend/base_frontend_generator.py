from agents.crud.generators.base_generator import BaseGenerator
from agents.crud.models.generation_context import GenerationContext


class BaseFrontendGenerator(BaseGenerator):
    """
    Clase base para todos los generadores React + TypeScript.

    Todos los generadores frontend deben heredar de esta clase.

    Responsabilidades:
    - Definir capa frontend.
    - Resolver nombres React.
    - Resolver nombres TypeScript.
    - Helpers comunes de componentes.
    - Imports React.
    - Convenciones de módulos.
    """

    # =====================================================
    # CAPA FRONTEND
    # =====================================================

    def layer(self) -> str:
        """
        Define que este generador pertenece al frontend.
        """

        return "frontend"

    # =====================================================
    # NOMBRES DE COMPONENTES
    # =====================================================

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

    # =====================================================
    # HOOKS
    # =====================================================

    def hook_name(
        self,
        context: GenerationContext,
    ) -> str:

        return f"use{self.pascal_name(context)}"

    # =====================================================
    # API / SERVICIOS
    # =====================================================

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

    # =====================================================
    # TYPESCRIPT
    # =====================================================

    def type_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.pascal_name(context)

    def ts_type(
        self,
        field,
    ) -> str:

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

        result = mapper.get(
            str(field.type).lower(),
            "any",
        )

        if getattr(field, "nullable", False):
            result = f"{result} | null"

        return result

    # =====================================================
    # CAMPOS INTERFACE TYPESCRIPT
    # =====================================================

    def interface_fields(
        self,
        context: GenerationContext,
    ) -> str:

        fields = []

        for field in context.fields:

            fields.append(f"    {field.name}: {self.ts_type(field)};")

        return "\n".join(fields)

    # =====================================================
    # VALORES INICIALES FORMULARIOS
    # =====================================================

    def default_values(
        self,
        context: GenerationContext,
    ) -> str:

        values = []

        for field in context.fields:

            field_type = self.ts_type(field)

            if field_type == "number":

                value = "0"

            elif field_type == "boolean":

                value = "false"

            else:

                value = "''"

            values.append(f"    {field.name}: {value},")

        return "\n".join(values)

    # =====================================================
    # IMPORTS REACT
    # =====================================================

    def react_imports(self) -> str:

        return (
            "import React from 'react';\n"
            "import { useEffect, useState } from 'react';"
        )

    def bootstrap_imports(self) -> str:

        return "import 'bootstrap/dist/css/bootstrap.min.css';"

    def axios_import(self) -> str:

        return "import axios from 'axios';"

    # =====================================================
    # MODULOS
    # =====================================================

    def module_name(
        self,
        context: GenerationContext,
    ) -> str:

        return self.snake_name(context)

    def module_path(
        self,
        context: GenerationContext,
    ) -> str:

        return f"modules/{self.snake_name(context)}"
