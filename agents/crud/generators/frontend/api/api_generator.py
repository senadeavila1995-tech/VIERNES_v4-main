from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class ApiGenerator(BaseFrontendGenerator):
    """
    Genera la capa API del frontend.

    Esta capa centraliza las llamadas HTTP
    relacionadas con la entidad.
    """

    name = "frontend_api"

    description = "Genera cliente API para React."

    order = 50

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.pascal_name(context)
        variable = self.camel_name(context)
        filename = self.snake_name(context)
        api = self.api_name(context)

        return f'''import axios from "axios";

import type {{ {entity} }} from "../types/{filename}";

const API_URL = "/api/{filename}";

export const {api} = {{

    async getAll(): Promise<{entity}[]> {{

        const response = await axios.get(API_URL);

        return response.data;

    }},

    async getById(id: number): Promise<{entity}> {{

        const response = await axios.get(
            `${{API_URL}}/${{id}}`
        );

        return response.data;

    }},

    async create(
        data: Omit<{entity}, "id">
    ): Promise<{entity}> {{

        const response = await axios.post(
            API_URL,
            data
        );

        return response.data;

    }},

    async update(
        id: number,
        data: Partial<{entity}>
    ): Promise<{entity}> {{

        const response = await axios.put(
            `${{API_URL}}/${{id}}`,
            data
        );

        return response.data;

    }},

    async delete(id: number): Promise<void> {{

        await axios.delete(
            `${{API_URL}}/${{id}}`
        );

    }},

}};
'''
