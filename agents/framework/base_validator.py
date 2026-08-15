class BaseValidator:
    """
    Validador base para todas las entidades.

    Cada Validator únicamente debe definir:

        schema = SCHEMA

    donde SCHEMA tiene el formato:

    SCHEMA = {
        "nombre": {
            "type": str,
            "required": True
        }
    }

    El validador acepta:
    - diccionarios
    - objetos con atributos
    - modelos Pydantic

    Soporta dos modos:

    validate(model)
        Validación completa. Los campos required deben existir.

    validate(model, partial=True)
        Validación parcial. Solo se validan los campos realmente
        presentes/enviados.
    """

    schema = {}

    @classmethod
    def validate(
        cls,
        model,
        partial=False,
    ) -> bool:
        """
        Valida una instancia o diccionario utilizando
        el esquema definido por la entidad.

        Cuando partial=True, solamente se validan los campos
        realmente presentes en el modelo.

        Esto permite diferenciar correctamente:

            {}
                -> campo no enviado

            {"campo": None}
                -> campo enviado explícitamente como NULL
        """

        missing = object()

        # ======================================================
        # Determinar campos realmente presentes
        # ======================================================

        if isinstance(model, dict):

            present_fields = set(model.keys())

        elif hasattr(model, "model_fields_set"):

            present_fields = set(
                model.model_fields_set
            )

        elif hasattr(model, "__dict__"):

            present_fields = {
                key
                for key in vars(model)
                if not key.startswith("_")
            }

        else:

            present_fields = {
                field
                for field in cls.schema
                if hasattr(model, field)
            }

        # ======================================================
        # Validar campos
        # ======================================================

        for field, config in cls.schema.items():

            required = config.get(
                "required",
                False,
            )

            expected = config.get(
                "type",
                object,
            )

            # ==================================================
            # UPDATE PARCIAL
            # ==================================================

            if partial and field not in present_fields:

                continue

            # ==================================================
            # Obtener valor
            # ==================================================

            if isinstance(model, dict):

                value = model.get(
                    field,
                    missing,
                )

            else:

                if not hasattr(model, field):

                    if required and not partial:

                        raise AttributeError(
                            f"El atributo '{field}' no existe en "
                            f"{model.__class__.__name__}."
                        )

                    continue

                value = getattr(
                    model,
                    field,
                )

            # ==================================================
            # Campo ausente
            # ==================================================

            if value is missing:

                if required and not partial:

                    raise ValueError(
                        f"'{field}' es obligatorio."
                    )

                continue

            # ==================================================
            # Campo obligatorio = None
            # ==================================================

            if required and value is None:

                raise ValueError(
                    f"'{field}' es obligatorio."
                )

            # ==================================================
            # Campo opcional = None
            # ==================================================

            if value is None:

                continue

            # ==================================================
            # Validación de tipo
            # ==================================================

            if not isinstance(
                value,
                expected,
            ):

                raise TypeError(
                    f"'{field}' debe ser de tipo "
                    f"{expected.__name__} "
                    f"y se recibió "
                    f"{type(value).__name__}."
                )

        return True
