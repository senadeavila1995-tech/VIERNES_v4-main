from pathlib import Path
import subprocess
import json
import shutil

from services.filesystem_service import FileSystemService


class WorkspaceAgent:

    def __init__(self):

        self.fs = FileSystemService()

        self.workspace = Path("workspace")
        self.workspace.mkdir(exist_ok=True)

        self.memory_file = self.workspace / "active_project.json"


    def create_project(self, name):

        project = self.workspace / name

        folders = [
            "app",
            "tests",
            "docs",
            "config",
            "logs",
            "data",
            "templates"
        ]


        project.mkdir(parents=True, exist_ok=True)


        for folder in folders:
            (project / folder).mkdir(exist_ok=True)


        files = [
            "README.md",
            "requirements.txt",
            ".gitignore",
            ".env"
        ]


        for file in files:
            (project / file).touch()


        self.set_active_project(name)


        return project



    def create_venv(self, project):

        subprocess.run(
            [
                "python3",
                "-m",
                "venv",
                "venv"
            ],
            cwd=project
        )



    def init_git(self, project):

        subprocess.run(
            [
                "git",
                "init"
            ],
            cwd=project
        )



    def open_vscode(self, project):

        subprocess.Popen(
            [
                "code",
                str(project)
            ]
        )



    def open_project(self, name):

        project = self.workspace / name


        if not project.exists():

            return {
                "success": False,
                "message": "Proyecto no encontrado"
            }


        self.set_active_project(name)

        self.open_vscode(project)


        return {
            "success": True,
            "project": name,
            "path": str(project)
        }



    def get_project(self, name):

        project = self.workspace / name


        if project.exists():

            return project


        return None



    def list_projects(self):

        return self.fs.list_projects()



    def set_active_project(self, name):

        data = {

            "project": name,

            "path": str(
                self.workspace / name
            )

        }


        self.memory_file.write_text(
            json.dumps(
                data,
                indent=4
            )
        )



    def get_active_project(self):

        if not self.memory_file.exists():

            return None


        return json.loads(
            self.memory_file.read_text()
        )



    def get_structure(self):

        active = self.get_active_project()


        if not active:

            return []


        project = Path(
            active["path"]
        )


        files = []


        for item in project.rglob("*"):

            if (
                ".git" not in item.parts
                and "venv" not in item.parts
            ):

                files.append(
                    str(
                        item.relative_to(project)
                    )
                )


        return files



    def read_file(self, filename):

        active = self.get_active_project()


        if not active:

            return None


        file = Path(
            active["path"]
        ) / filename



        if file.exists():

            return file.read_text(
                encoding="utf-8"
            )


        return None



    def write_file(self, filename, content):

        active = self.get_active_project()


        if not active:

            return False



        file = Path(
            active["path"]
        ) / filename



        # Crear backup antes de modificar

        if file.exists():

            backup = file.with_suffix(
                file.suffix + ".backup"
            )

            shutil.copy(
                file,
                backup
            )



        file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        file.write_text(
            content,
            encoding="utf-8"
        )


        return True



    def delete_file(self, filename):

        active = self.get_active_project()


        if not active:

            return False


        file = Path(
            active["path"]
        ) / filename



        if file.exists():

            file.unlink()

            return True


        return False
    def get_file_context(self, filename):

        content = self.read_file(filename)

        if not content:
            return None


        return {
            "file": filename,
            "content": content
        }