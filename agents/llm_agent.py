from services.llm.llm_manager import LLMManager


class LLMAgent:
    """
    Agente encargado de comunicarse con los modelos LLM.

    No interpreta intenciones.
    No crea planes.
    No ejecuta acciones.

    Solo envía mensajes al proveedor configurado.
    """

    def __init__(self):

        self.manager = LLMManager()


    # =====================================================
    # CONSULTA GENERAL
    # =====================================================

    def ask(
        self,
        messages,
        provider=None
    ):

        return self.manager.ask(
            prompt=messages,
            provider=provider
        )


    # =====================================================
    # GENERAR CÓDIGO
    # =====================================================

    def generate_code(
        self,
        prompt,
        provider=None
    ):

        messages = [

            {
                "role": "system",
                "content": (
                    "Eres un desarrollador Senior. "
                    "Devuelve únicamente código válido. "
                    "No expliques nada."
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

        return self.ask(
            messages,
            provider
        )


    # =====================================================
    # CHAT
    # =====================================================

    def chat(
        self,
        text,
        provider=None
    ):

        messages = [

            {
                "role": "user",
                "content": text
            }

        ]

        return self.ask(
            messages,
            provider
        )


    # =====================================================
    # EXPLICAR CÓDIGO
    # =====================================================

    def explain(
        self,
        code,
        provider=None
    ):

        messages = [

            {
                "role": "system",
                "content": (
                    "Explica el siguiente código "
                    "de forma clara y resumida."
                )
            },

            {
                "role": "user",
                "content": code
            }

        ]

        return self.ask(
            messages,
            provider
        )


    # =====================================================
    # REVISAR CÓDIGO
    # =====================================================

    def review_code(
        self,
        code,
        provider=None
    ):

        messages = [

            {
                "role": "system",
                "content": (
                    "Revisa el siguiente código. "
                    "Encuentra errores, problemas de seguridad "
                    "y posibles mejoras."
                )
            },

            {
                "role": "user",
                "content": code
            }

        ]

        return self.ask(
            messages,
            provider
        )


    # =====================================================
    # CORREGIR CÓDIGO
    # =====================================================

    def fix_code(
        self,
        code,
        error,
        provider=None
    ):

        messages = [

            {
                "role": "system",
                "content": (
                    "Corrige el código utilizando el error "
                    "proporcionado. Devuelve únicamente "
                    "el código completo corregido."
                )
            },

            {
                "role": "user",
                "content": f"""

ERROR:

{error}


CÓDIGO:

{code}

"""
            }

        ]

        return self.ask(
            messages,
            provider
        )
    
        # =====================================================
    # MODIFICAR ARCHIVO DEL WORKSPACE
    # =====================================================

    def ask_code(
        self,
        filename,
        code,
        request,
        provider=None
    ):

        messages = [

            {
                "role": "system",
                "content": (
                    "Eres un desarrollador Senior. "
                    "Modifica código existente. "
                    "Mantén la estructura actual. "
                    "Devuelve únicamente el código completo "
                    "sin explicaciones ni markdown."
                )
            },

            {
                "role": "user",
                "content": f"""

ARCHIVO:
{filename}


CÓDIGO ACTUAL:

{code}


CAMBIO SOLICITADO:

{request}


Genera el archivo completo actualizado.
"""
            }

        ]


        return self.ask(
            messages,
            provider
        )