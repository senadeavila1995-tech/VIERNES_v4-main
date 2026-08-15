from agents.memory_agent import MemoryAgent
from models.action_result import ActionResult
from services.documents.document_service import DocumentService


class DocumentAgent:

    def __init__(self):

        self.documents = DocumentService()

        self.memory = MemoryAgent()


    # ==================================================
    # CREAR DOCUMENTO
    # ==================================================

    def create_document(self, path):

        self.documents.create(path)

        self.memory.update_document(path)

        return ActionResult(
            success=True,
            message=f"Documento creado: {path}"
        )


    # ==================================================
    # ESCRIBIR DOCUMENTO
    # ==================================================

    def write_document(self, path, text):

        current = self.documents.read(path)


        if current.strip():

            return ActionResult(
                success=False,
                message="El documento ya contiene información.",
                next_question="¿Deseas reemplazar el contenido?"
            )


        self.documents.write(
            path,
            text
        )


        self.memory.update_document(path)


        return ActionResult(
            success=True,
            message="Documento guardado correctamente."
        )


    # ==================================================
    # AGREGAR CONTENIDO
    # ==================================================

    def append_document(self, path, text):

        self.documents.append(
            path,
            text
        )


        self.memory.update_document(path)


        return ActionResult(
            success=True,
            message="Contenido agregado al documento."
        )


    # ==================================================
    # INSERTAR LÍNEA
    # ==================================================

    def insert_document(
        self,
        path,
        line,
        text
    ):

        self.documents.insert_line(
            path,
            line,
            text
        )


        self.memory.update_document(path)


        return ActionResult(
            success=True,
            message=f"Contenido insertado en la línea {line}."
        )