from pathlib import Path

from agents.workspace_agent import WorkspaceAgent
from agents.memory_agent import MemoryAgent
from agents.document_agent import DocumentAgent
from agents.terminal_agent import TerminalAgent
from agents.code_agent import CodeAgent
from agents.llm_agent import LLMAgent
from agents.scanner_agent import ScannerAgent

from agents.crud.crud_agent import CrudAgent
from agents.crud.models.crud_definition import CrudDefinition
from agents.crud.models.project_context import ProjectContext
from agents.crud.models.generation_context import GenerationContext
from agents.crud.models.crud_field import CrudField


class Router:

    def __init__(self):

        self.scanner = ScannerAgent()
        self.workspace = WorkspaceAgent()
        self.memory = MemoryAgent()
        self.documents = DocumentAgent()
        self.terminal = TerminalAgent()
        self.code = CodeAgent()

        # ======================================================
        # LLM OPCIONAL
        # ======================================================

        try:

            self.llm = LLMAgent()

        except Exception as error:

            self.llm = None

            print(
                f"LLM deshabilitado: {error}"
            )


        # CRUD Generator
        self.crud = CrudAgent()

        self.routes = {
            # ==========================
            # Workspace
            # ==========================
            "scan_project": self.scan_project,
            "create_project": self.create_project,
            "list_projects": self.list_projects,
            "create_venv": self.create_venv,
            "init_git": self.init_git,
            "open_vscode": self.open_vscode,
            "open_project": self.open_project,
            "get_structure": self.get_structure,
            "read_file": self.read_file,
            "write_file": self.write_file,
            # ==========================
            # Documentos
            # ==========================
            "create_document": self.create_document,
            "write_document": self.write_document,
            "append_document": self.append_document,
            "insert_document": self.insert_document,
            # ==========================
            # IA
            # ==========================
            "ask_llm": self.ask_llm,
            "generate_code": self.generate_code,
            "review_code": self.review_code,
            "explain_code": self.explain_code,
            # ==========================
            # Terminal
            # ==========================
            "run_terminal": self.run_terminal,
            # ==========================
            # CRUD
            # ==========================
            "create_crud": self.create_crud,
            # ==========================
            # Futuro
            # ==========================
            "delete_project": self.delete_project,
            "rename_project": self.rename_project,
        }

    # ==========================================================
    # Dispatcher
    # ==========================================================

    def dispatch_step(self, task):

        self.memory.update_last_action(task.action)

        action = self.routes.get(task.action)

        if action is None:

            return {
                "success": False,
                "message": f"La acción '{task.action}' no existe.",
            }

        try:

            result = action(task)

            if isinstance(result, dict):

                return result

            return {"success": True, "message": result}

        except Exception as e:

            return {"success": False, "message": str(e)}

    # ==========================================================
    # Workspace
    # ==========================================================

    def scan_project(self, task):

        project = self.memory.get_context().current_project

        if not project:

            return {"success": False, "message": "No existe proyecto activo."}

        data = self.scanner.scan_project(f"workspace/{project}")

        return {"success": True, "scan": data}

    def create_project(self, task):

        name = task.parameters.get("name")

        if not name:

            return {"success": False, "message": "Debes indicar nombre."}

        project = self.workspace.create_project(name)

        self.memory.update_project(name)

        return {
            "success": True,
            "project": name,
            "path": str(project),
            "message": f"Proyecto '{name}' creado correctamente.",
        }

    def list_projects(self, task):

        return {"success": True, "projects": self.workspace.list_projects()}

    def create_venv(self, task):

        project = self.memory.get_context().current_project

        if not project:

            return {"success": False, "message": "No existe proyecto activo."}

        self.workspace.create_venv(f"workspace/{project}")

        return {"success": True, "message": "Entorno virtual creado."}

    def init_git(self, task):

        project = self.memory.get_context().current_project

        if not project:

            return {"success": False, "message": "No existe proyecto activo."}

        self.workspace.init_git(f"workspace/{project}")

        return {"success": True, "message": "Repositorio Git inicializado."}

    def open_vscode(self, task):

        project = self.memory.get_context().current_project

        if not project:

            return {"success": False, "message": "No existe proyecto activo."}

        self.workspace.open_vscode(f"workspace/{project}")

        return {"success": True, "message": "Proyecto abierto."}

    def open_project(self, task):

        name = task.parameters.get("name")

        result = self.workspace.open_project(name)

        if result.get("success"):

            self.memory.update_project(name)

        return result

    def get_structure(self, task):

        return {"success": True, "files": self.workspace.get_structure()}

    def read_file(self, task):

        filename = task.parameters.get("filename")

        content = self.workspace.read_file(filename)

        return {"success": True, "filename": filename, "content": content}

    def write_file(self, task):

        result = self.workspace.write_file(
            task.parameters.get("filename"), task.parameters.get("content")
        )

        return {"success": result, "message": "Archivo actualizado."}

    # ==========================================================
    # Documentos
    # ==========================================================

    def create_document(self, task):

        return self.documents.create_document(task.parameters.get("path"))

    def write_document(self, task):

        return self.documents.write_document(
            task.parameters.get("path"), task.parameters.get("text")
        )

    def append_document(self, task):

        return self.documents.append_document(
            task.parameters.get("path"), task.parameters.get("text")
        )

    def insert_document(self, task):

        return self.documents.insert_document(
            task.parameters.get("path"),
            task.parameters.get("line"),
            task.parameters.get("text"),
        )

    # ==========================================================
    # IA
    # ==========================================================

    def ask_llm(self, task):

        if self.llm is None:

            return {
                "success": False,
                "message": "LLM no disponible. Configure OPENAI_API_KEY.",
            }

        return {
            "success": True,
            "response": self.llm.chat(
                task.parameters.get("prompt")
            ),
        }


    def generate_code(self, task):

        if self.llm is None:

            return {
                "success": False,
                "message": "LLM no disponible. Configure OPENAI_API_KEY.",
            }

        return {
            "success": True,
            "code": self.llm.generate_code(
                task.parameters.get("prompt")
            ),
        }


    def review_code(self, task):

        if self.llm is None:

            return {
                "success": False,
                "message": "LLM no disponible. Configure OPENAI_API_KEY.",
            }

        return {
            "success": True,
            "review": self.llm.review_code(
                task.parameters.get("code")
            ),
        }


    def explain_code(self, task):

        if self.llm is None:

            return {
                "success": False,
                "message": "LLM no disponible. Configure OPENAI_API_KEY.",
            }

        return {
            "success": True,
            "explanation": self.llm.explain(
                task.parameters.get("code")
            ),
        }

    # ==========================================================
    # Terminal
    # ==========================================================

    def run_terminal(self, task):

        return self.terminal.run(task.parameters.get("command"))

    # ==========================================================
    # CRUD GENERATOR
    # ==========================================================

    def create_crud(self, task):

        parameters = task.parameters

        entity = parameters.get("entity")
        table = parameters.get("table")
        fields_data = parameters.get("fields", [])

        if not entity:

            return {"success": False, "message": "Falta entidad."}

        if not table:

            return {"success": False, "message": "Falta tabla."}

        # ==========================================================
        # Construcción de campos
        # ==========================================================

        fields: list[CrudField] = []

        # ----------------------------------------------------------
        # Llave primaria automática
        # ----------------------------------------------------------

        fields.append(
            CrudField(
                name="id",
                type="integer",
                primary_key=True,
                auto_increment=True,
                required=True,
                unique=True,
            )
        )

        # ----------------------------------------------------------
        # Campos definidos por el usuario
        # ----------------------------------------------------------

        for item in fields_data:

            name = item.get("name")
            field_type = item.get("type")


            # La PK id ya fue creada automáticamente arriba
            if name == "id":
                continue


            foreign_key = False
            references = None

            # Detectar automáticamente relaciones
            if name.endswith("_id"):

                foreign_key = True
                references = name.removesuffix("_id") + "s"

            # Resolver nulabilidad automáticamente
            nullable = item.get("nullable", False)

            required = item.get(
                "required",
                not nullable
            )


            fields.append(
                CrudField(
                    name=name,
                    type=field_type,
                    description=item.get("description", ""),
                    required=required,
                    nullable=nullable,
                    unique=item.get("unique", False),
                    default=item.get("default"),
                    primary_key=item.get("primary_key", False),
                    auto_increment=item.get("auto_increment", False),
                    length=item.get("length"),
                    precision=item.get("precision"),
                    scale=item.get("scale"),
                    enum=item.get("enum"),
                    foreign_key=foreign_key,
                    references=references,
                    references_field=item.get("references_field", "id"),
                    on_delete=item.get("on_delete"),
                    on_update=item.get("on_update"),
                    index=item.get("index", False),
                    check=item.get("check"),
                )
            )

        definition = CrudDefinition(
            entity=entity,
            table=table,
            fields=fields,
        )

        current_project = self.memory.get_context().current_project

        project_name = current_project if current_project else "generated_crud"

        project = ProjectContext(
            project_name=project_name,
            root_path=Path(f"workspace/{project_name}"),
            language="python",
            framework="fastapi",
            database="mysql",
            orm="sqlalchemy",
        )

        self.memory.register_crud_definition(
            entity,
            definition,
        )


        definitions = self.memory.get_crud_definitions()


        context = GenerationContext(
            definition=definition,
            project=project,
            definitions=definitions,
        )

        print("=" * 60)
        print("CRUD ROUTER DEBUG")
        print("ENTITY:", context.definition.entity)
        print(
            "FIELDS:",
            [
                field.name
                for field in context.fields
            ]
        )
        print(
            "DEFINITIONS:",
            list(context.definitions.keys())
        )
        print("=" * 60)

        return self.crud.execute(context)

    # ==========================================================
    # Futuro
    # ==========================================================

    def delete_project(self, task):

        return {"success": False, "message": "Pendiente."}

    def rename_project(self, task):

        return {"success": False, "message": "Pendiente."}
