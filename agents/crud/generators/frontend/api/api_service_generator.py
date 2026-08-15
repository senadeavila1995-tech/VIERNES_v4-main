from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext


class ApiServiceGenerator(BaseFrontendGenerator):

    name = "api_service"

    description = "Genera servicios API para React."

    order = 60

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        entity = self.pascal_name(context)
        variable = self.camel_name(context)
        service = self.service_name(context)

        return f'''import axios from "axios";

import type {{ {entity} }} from "../types/{variable}";


const API_URL = "/api/{variable}";


export const {service} = {{

    async getAll(): Promise<{entity}[]> {{

        const response = await axios.get(API_URL);

        return response.data;

    }},

    async getById(id: number): Promise<{entity}> {{

        const response = await axios.get(`${{API_URL}}/${{id}}`);

        return response.data;

    }},

    async create(data: Omit<{entity}, "id">): Promise<{entity}> {{

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