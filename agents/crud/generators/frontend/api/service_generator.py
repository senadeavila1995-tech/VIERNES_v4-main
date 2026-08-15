from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class ServiceGenerator(BaseFrontendGenerator):
    """
    Genera la capa de servicio del frontend.

    El Service utiliza la API generada
    para encapsular las operaciones CRUD.
    """

    name = "frontend_service"

    description = "Genera servicio CRUD para React."

    order = 60

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.pascal_name(context)
        filename = self.snake_name(context)
        api = self.api_name(context)
        service = self.service_name(context)

        api_file = f"{filename}_api"

        return f'''import type {{ {entity} }} from "../types/{filename}";

import {{ {api} }} from "../api/{api_file}";

export const {service} = {{

    async getAll(): Promise<{entity}[]> {{

        return {api}.getAll();

    }},

    async getById(
        id: number
    ): Promise<{entity}> {{

        return {api}.getById(id);

    }},

    async create(
        data: Omit<{entity}, "id">
    ): Promise<{entity}> {{

        return {api}.create(data);

    }},

    async update(
        id: number,
        data: Partial<{entity}>
    ): Promise<{entity}> {{

        return {api}.update(id, data);

    }},

    async delete(
        id: number
    ): Promise<void> {{

        return {api}.delete(id);

    }},

}};
'''
