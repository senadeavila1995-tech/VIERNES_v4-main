from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class HookGenerator(BaseFrontendGenerator):
    """
    Genera el hook principal del módulo CRUD.

    El hook centraliza:
    - carga de registros
    - creación
    - actualización
    - eliminación
    """

    name = "hook"

    description = "Genera hook CRUD para React."

    order = 70

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.pascal_name(context)
        variable = self.camel_name(context)
        filename = self.snake_name(context)
        service = self.service_name(context)
        hook = self.hook_name(context)

        service_file = f"{filename}_service"

        return f'''import {{ useCallback, useEffect, useState }} from "react";

import type {{ {entity} }} from "../types/{filename}";

import {{ {service} }} from "../services/{service_file}";

export function {hook}() {{

    const [{variable}, set{entity}] = useState<{entity}[]>([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState<string | null>(null);

    const load = useCallback(async () => {{

        try {{

            setLoading(true);

            setError(null);

            const data = await {service}.getAll();

            set{entity}(data);

        }} catch (err) {{

            console.error(err);

            setError(
                "No fue posible cargar los registros."
            );

        }} finally {{

            setLoading(false);

        }}

    }}, []);

    const create = async (
        data: Omit<{entity}, "id">
    ) => {{

        await {service}.create(data);

        await load();

    }};

    const update = async (
        id: number,
        data: Partial<{entity}>
    ) => {{

        await {service}.update(
            id,
            data
        );

        await load();

    }};

    const remove = async (
        id: number
    ) => {{

        await {service}.delete(id);

        await load();

    }};

    useEffect(() => {{

        load();

    }}, [load]);

    return {{

        {variable},

        loading,

        error,

        load,

        create,

        update,

        remove,

    }};
}}
'''

    def folder(self) -> str:
        return "hooks"

    def filename(
        self,
        context: GenerationContext,
    ) -> str:

        return f"{self.hook_name(context)}.ts"
