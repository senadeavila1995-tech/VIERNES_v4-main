import json
from pathlib import Path

from core.context import Context


class MemoryAgent:

    FILE = Path("memory/context.json")


    def __init__(self):

        self.FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.FILE.exists():

            self.FILE.write_text(
                "{}",
                encoding="utf-8"
            )

        self.context = Context()

        self.load()



    # ==========================================================
    # CARGAR MEMORIA
    # ==========================================================

    def load(self):

        try:

            data = json.loads(
                self.FILE.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            data = {}


        self.context.current_project = data.get(
            "current_project"
        )

        self.context.project_path = data.get(
            "project_path"
        )

        self.context.language = data.get(
            "language"
        )

        self.context.framework = data.get(
            "framework"
        )

        self.context.frontend = data.get(
            "frontend"
        )

        self.context.database = data.get(
            "database"
        )


        self.context.current_document = data.get(
            "current_document"
        )

        self.context.opened_files = data.get(
            "opened_files",
            []
        )


        self.context.provider = data.get(
            "provider",
            "openai"
        )


        # Nueva arquitectura Task
        self.context.last_action = data.get(
            "last_action"
        )


        self.context.scanned = data.get(
            "scanned",
            False
        )

        self.context.project_index = data.get(
            "project_index",
            {}
        )


        self.context.crud_definitions = data.get(
            "crud_definitions",
            {}
        )



    # ==========================================================
    # GUARDAR MEMORIA
    # ==========================================================

    def save(self):

        data = {

            "current_project":
                self.context.current_project,

            "project_path":
                self.context.project_path,

            "language":
                self.context.language,

            "framework":
                self.context.framework,

            "frontend":
                self.context.frontend,

            "database":
                self.context.database,


            "current_document":
                self.context.current_document,

            "opened_files":
                self.context.opened_files,


            "provider":
                self.context.provider,


            "last_action":
                self.context.last_action,


            "scanned":
                self.context.scanned,


            "project_index":
                self.context.project_index,
        }


        self.FILE.write_text(

            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ),

            encoding="utf-8"

        )



    # ==========================================================
    # PROYECTO
    # ==========================================================

    def update_project(self, project):

        self.context.current_project = project

        self.context.project_path = (
            f"workspace/{project}"
        )

        self.save()



    def update_project_path(self, path):

        self.context.project_path = path

        self.save()



    def update_language(self, language):

        self.context.language = language

        self.save()



    def update_framework(self, framework):

        self.context.framework = framework

        self.save()



    def update_frontend(self, frontend):

        self.context.frontend = frontend

        self.save()



    def update_database(self, database):

        self.context.database = database

        self.save()



    # ==========================================================
    # DOCUMENTOS
    # ==========================================================

    def update_document(self, document):

        self.context.current_document = document

        self.save()



    def add_opened_file(self, path):

        if path not in self.context.opened_files:

            self.context.opened_files.append(path)

            self.save()



    def remove_opened_file(self, path):

        if path in self.context.opened_files:

            self.context.opened_files.remove(path)

            self.save()



    def clear_opened_files(self):

        self.context.opened_files.clear()

        self.save()



    # ==========================================================
    # IA
    # ==========================================================

    def update_provider(self, provider):

        self.context.provider = provider

        self.save()



    # ==========================================================
    # TASK / PLANNER
    # ==========================================================

    def update_last_action(self, action):

        self.context.last_action = action

        self.save()



    # ==========================================================
    # SCANNER
    # ==========================================================

    def update_project_index(self, index):

        self.context.project_index = index

        self.context.scanned = True

        self.save()



    def clear_project_index(self):

        self.context.project_index = {}

        self.context.scanned = False

        self.save()



    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def register_crud_definition(
        self,
        entity: str,
        definition,
    ):

        self.context.crud_definitions[entity] = definition


    def get_crud_definitions(self):

        return self.context.crud_definitions


    def get_context(self):

        return self.context


    def get_project(self):

        return self.context.current_project


    def get_project_path(self):

        return self.context.project_path


    def get_provider(self):

        return self.context.provider


    def get_project_index(self):

        return self.context.project_index


    def is_project_scanned(self):

        return self.context.scanned



    # ==========================================================
    # EXPORTAR
    # ==========================================================

    def to_dict(self):

        return {

            "current_project":
                self.context.current_project,

            "project_path":
                self.context.project_path,

            "language":
                self.context.language,

            "framework":
                self.context.framework,

            "frontend":
                self.context.frontend,

            "database":
                self.context.database,

            "current_document":
                self.context.current_document,

            "opened_files":
                self.context.opened_files,

            "provider":
                self.context.provider,

            "last_action":
                self.context.last_action,

            "scanned":
                self.context.scanned,

            "project_index":
                self.context.project_index,
        }



    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        self.context = Context()

        self.save()