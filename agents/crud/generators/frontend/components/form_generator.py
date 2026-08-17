from agents.crud.generators.frontend.base_frontend_generator import (
    BaseFrontendGenerator,
)

from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.naming_resolver import NamingResolver


class FormGenerator(BaseFrontendGenerator):

    name = "frontend_form"

    description = (
        "Genera formulario React con soporte para claves foráneas."
    )

    order = 90

    def generate_content(
        self,
        context: GenerationContext,
    ) -> str:

        component = self.form_name(context)
        entity_pascal = self.pascal_name(context)
        entity_camel = self.camel_name(context)
        entity_snake = self.snake_name(context)

        # ==========================================================
        # IMPORTS
        # ==========================================================

        imports = [
            'import { useEffect, useState } from "react";',
            f'import type {{ {entity_pascal} }} '
            f'from "../types/{entity_snake}";',
            f'import type {{ {entity_pascal}Create }} '
            f'from "../types/{entity_snake}_create";',
            f'import {{ {entity_camel}Service }} '
            f'from "../services/{entity_snake}_service";',
        ]

        states = []
        effects = []
        inputs = []

        processed_references = set()

        # ==========================================================
        # FOREIGN KEYS
        # ==========================================================

        for field in context.fields:

            field_name = field.name

            if (
                getattr(field, "primary_key", False)
                and getattr(field, "auto_increment", False)
            ):
                continue

            if (
                getattr(field, "foreign_key", False)
                and getattr(field, "references", None)
            ):

                reference = field.references

                # Normalizar referencias de tablas pluralizadas
                # categorias -> categoria
                reference = reference.rstrip("s")

                reference_variable = NamingResolver.camel(
                    field_name.replace("_id", "")
                )

                reference_type = NamingResolver.pascal(
                    reference
                )

                reference_module = NamingResolver.snake(
                    reference
                )

                service_name = f"{reference_variable}Service"

                # --------------------------------------------------
                # IMPORTAR UNA SOLA VEZ CADA REFERENCIA
                # --------------------------------------------------

                relation_key = f"{field_name}:{reference}"

                if relation_key not in processed_references:

                    imports.append(
                        f'import type {{ {reference_type} }} '
                        f'from "../../{reference_module}/types/'
                        f'{reference_module}";'
                    )

                    imports.append(
                        f'import {{ {service_name} }} '
                        f'from "../../{reference_module}/services/'
                        f'{reference_module}_service";'
                    )

                    states.append(
                        f"    const [{reference_variable}, "
                        f"set{NamingResolver.pascal(reference_variable)}] = "
                        f"useState<{reference_type}[]>([]);"
                    )

                    effects.append(
                        f'''        {service_name}.getAll()
        .then(set{NamingResolver.pascal(reference_variable)})
        .catch((error) => {{
            console.error(
                "No fue posible cargar {reference_variable}.",
                error
            );
        }});'''
                    )

                    processed_references.add(relation_key)

                label = self._field_label(field_name)

                references_field = getattr(
                    field,
                    "references_field",
                    "id",
                )

                display_field = self._find_display_field(
                    reference,
                    references_field,
                    context,
                )

                nullable = getattr(
                    field,
                    "nullable",
                    False,
                )

                nullable_option_value = (
                    ""
                    if nullable
                    else "0"
                )

                nullable_option_label = (
                    f"Sin {label.lower()}"
                    if nullable
                    else f"Seleccione {label.lower()}"
                )

                inputs.append(
                    f'''        <div className="mb-3">

        <label className="form-label">
            {label}
        </label>

        <select
            className="form-select"
            name="{field_name}"
            value={{formData.{field_name}}}
            onChange={{handleChange}}
        >

            <option value="{nullable_option_value}">
                {nullable_option_label}
            </option>

            {{Array.isArray({reference_variable}) &&
                {reference_variable}.map((item) => (
                    <option
                        key={{item.{references_field}}}
                        value={{item.{references_field}}}
                    >
                        {{item.{display_field} || item.{references_field}}}
                    </option>
                ))
            }}

        </select>

    </div>'''
                )

                continue

            # ==================================================
            # CAMPO NORMAL
            # ==================================================

            label = self._field_label(field_name)
            input_type = self._input_type(field)

            if input_type == "checkbox":

                inputs.append(
                    f'''        <div className="mb-3 form-check">

        <input
            type="checkbox"
            className="form-check-input"
            name="{field_name}"
            checked={{formData.{field_name}}}
            onChange={{handleChange}}
        />

        <label className="form-check-label">
            {label}
        </label>

    </div>'''
                )

            else:

                inputs.append(
                    f'''        <div className="mb-3">

        <label className="form-label">
            {label}
        </label>

        <input
            type="{input_type}"
            className="form-control"
            name="{field_name}"
            value={{formData.{field_name}}}
            onChange={{handleChange}}
        />

    </div>'''
                )

        # ==========================================================
        # CONTENIDO
        # ==========================================================

        imports_content = "\n".join(imports)
        states_content = "\n".join(states)
        effects_content = "\n\n".join(effects)
        body = "\n\n".join(inputs)

        # ==========================================================
        # VALORES INICIALES
        # ==========================================================

        initial_values = []

        for field in context.fields:

            if (
                getattr(field, "primary_key", False)
                and getattr(field, "auto_increment", False)
            ):
                continue

            field_type = self.ts_type(field)

            nullable = getattr(
                field,
                "nullable",
                False,
            )

            if getattr(field, "foreign_key", False):

                if nullable:
                    value = "null"
                else:
                    value = "0"

            elif field_type == "number":

                if nullable:
                    value = "null"
                else:
                    value = "0"

            elif field_type == "boolean":
                value = "false"

            else:
                value = "''"

            initial_values.append(
                f"        {field.name}: {value},"
            )

        initial_values_content = "\n".join(
            initial_values
        )

        # ==========================================================
        # CAMPOS NUMERICOS
        # ==========================================================

        numeric_fields = []

        for field in context.fields:

            if (
                getattr(field, "primary_key", False)
                and getattr(field, "auto_increment", False)
            ):
                continue

            if "number" in self.ts_type(field):

                numeric_fields.append(
                    field.name
                )

        # ==========================================================
        # HANDLE CHANGE
        # ==========================================================

        if numeric_fields:

            numeric_names = repr(
                numeric_fields
            )

            numeric_condition_input = (
                f"({numeric_names} as string[]).includes(name)"
            )

            numeric_condition_select = (
                f"({numeric_names} as string[]).includes(name)"
            )

        else:

            numeric_condition_input = "false"
            numeric_condition_select = "false"

        # ==========================================================
        # PAYLOAD NUMERIC
        # ==========================================================

        numeric_payload = []

        for field_name in numeric_fields:

            field = next(
                (
                    item
                    for item in context.fields
                    if item.name == field_name
                ),
                None,
            )

            nullable = getattr(
                field,
                "nullable",
                False,
            )

            if nullable:

                numeric_payload.append(
                    f'''            {field_name}:
                formData.{field_name}
                    ? Number(formData.{field_name})
                    : null,'''
                )

            else:

                numeric_payload.append(
                    f'''            {field_name}:
                Number(formData.{field_name}),'''
                )

        numeric_payload_content = "\n".join(
            numeric_payload
        )

        # ==========================================================
        # USE EFFECT
        # ==========================================================

        use_effect = ""

        if effects_content:

            use_effect = f'''
    useEffect(() => {{

{effects_content}

    }}, []);
'''

        # ==========================================================
        # RETURN
        # ==========================================================

        return f'''{imports_content}

interface Props {{

    data?: {entity_pascal};

    onSaved?: () => void | Promise<void>;

}}

export default function {component}({{

    data,

    onSaved

}}: Props) {{

{states_content}

    const [formData, setFormData] = useState<{entity_pascal}Create>({{
{initial_values_content}
    }});

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");


    useEffect(() => {{

        if(data) {{

            setFormData({{
                ...data
            }});

        }}

    }}, [data]);


{use_effect}

    const handleChange = (
        event: React.ChangeEvent<
            HTMLInputElement | HTMLSelectElement
        >
    ) => {{

        const {{ name, value }} = event.target;

        const target = event.target;

        let parsedValue: string | number | boolean | null = value;

        if (target instanceof HTMLInputElement) {{

            if (target.type === "checkbox") {{

                parsedValue = target.checked;

            }} else if ({numeric_condition_input}) {{

                parsedValue = Number(value);

            }}

        }} else if ({numeric_condition_select}) {{

            parsedValue = value === ""
                ? null
                : Number(value);

        }}

        setFormData((previous) => ({{
            ...previous,
            [name]: parsedValue,
        }}));

    }};

    const handleSubmit = async (
        event: React.FormEvent<HTMLFormElement>
    ) => {{

        event.preventDefault();

        setLoading(true);

        setError("");

        try {{

            const payload = {{
                ...formData,
{numeric_payload_content}
            }};

            if(data?.id) {{

                await {entity_camel}Service.update(
                    data.id,
                    payload
                );

            }} else {{

                await {entity_camel}Service.create(
                    payload
                );

            }}

            await onSaved?.();

            setFormData({{
{initial_values_content}
            }});

        }} catch (error) {{

            console.error(
                "No fue posible guardar {entity_camel}.",
                error
            );

            setError(
                "No fue posible guardar el registro."
            );

        }} finally {{

            setLoading(false);

        }}

    }};

    return (

        <form onSubmit={{handleSubmit}}>

            {{error && (
                <div className="alert alert-danger">
                    {{error}}
                </div>
            )}}

{body}

            <button
                type="submit"
                className="btn btn-primary"
                disabled={{loading}}
            >
                {{loading ? "Guardando..." : "Guardar"}}
            </button>

        </form>

    );

}}

'''

    # ==========================================================
    # DISPLAY FIELD
    # ==========================================================

    def _find_display_field(
        self,
        reference: str,
        references_field: str,
        context: GenerationContext,
    ) -> str:

        """
        Determina el campo que debe mostrarse en un select FK.

        La resolución se basa primero en los campos disponibles
        de la entidad referenciada cuando están disponibles en
        el contexto. Para los casos habituales de VIERNES se
        utilizan nombres convencionales.
        """

        candidates = (
            "nombre",
            "name",
            "descripcion",
            "description",
            "titulo",
            "title",
            "codigo",
            "code",
        )

        # ----------------------------------------------------------
        # Intentar encontrar información de la entidad referenciada
        # en las dependencias del contexto.
        # ----------------------------------------------------------

        definitions = getattr(
            context,
            "definitions",
            {},
        )

        if isinstance(definitions, dict):

            dependency = None

            # --------------------------------------------------
            # Resolver entidad relacionada.
            #
            # Puede venir como:
            # categoria
            # Categoria
            # categorias
            # --------------------------------------------------

            possible_names = [
                reference,
                NamingResolver.pascal(reference),
                NamingResolver.snake(reference),
                f"{reference}s",
                NamingResolver.pascal(reference) + "s",
            ]

            for name in possible_names:

                if name in definitions:
                    dependency = definitions[name]
                    break


            if dependency is not None:

                fields = getattr(
                    dependency,
                    "fields",
                    [],
                )

                field_names = {
                    getattr(field, "name", "")
                    for field in fields
                }

                for candidate in candidates:

                    if candidate in field_names:
                        return candidate

                if references_field in field_names:
                    return references_field

        # ----------------------------------------------------------
        # Fallback seguro.
        # ----------------------------------------------------------

        return references_field

    # ==========================================================
    # LABEL
    # ==========================================================

    def _field_label(
        self,
        field_name: str,
    ) -> str:

        label = field_name.replace(
            "_id",
            "",
        )

        label = label.replace(
            "_",
            " ",
        )

        return label.capitalize()

    # ==========================================================
    # INPUT TYPE
    # ==========================================================

    def _input_type(
        self,
        field,
    ) -> str:

        field_type = str(
            getattr(field, "type", "")
        ).lower()

        if field_type in (
            "int",
            "integer",
            "bigint",
            "float",
            "double",
            "decimal",
        ):
            return "number"

        if field_type == "date":
            return "date"

        if field_type in (
            "datetime",
            "timestamp",
        ):
            return "datetime-local"

        if field_type in (
            "boolean",
            "bool",
        ):
            return "checkbox"

        return "text"

    # ==========================================================
    # CAMEL CASE
    # ==========================================================

    def _to_camel_case(
        self,
        value: str,
    ) -> str:

        parts = (
            value
            .replace("-", "_")
            .split("_")
        )

        if not parts:
            return value

        return (
            parts[0].lower()
            + "".join(
                part.capitalize()
                for part in parts[1:]
            )
        )

    # ==========================================================
    # PASCAL CASE
    # ==========================================================

    def _pascal_case(
        self,
        value: str,
    ) -> str:

        parts = (
            value
            .replace("-", "_")
            .split("_")
        )

        return "".join(
            part.capitalize()
            for part in parts
            if part
        )

    # ==========================================================
    # SNAKE CASE
    # ==========================================================

    def _to_snake_case(
        self,
        value: str,
    ) -> str:

        return value.replace(
            "-",
            "_",
        ).lower()
