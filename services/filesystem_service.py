from pathlib import Path
import shutil


class FileSystemService:

    ROOT = Path("workspace")

    def ensure_workspace(self):

        self.ROOT.mkdir(exist_ok=True)

    def create_folder(self, path):

        Path(path).mkdir(parents=True, exist_ok=True)

    def create_file(self, path):

        Path(path).touch(exist_ok=True)

    def exists(self, path):

        return Path(path).exists()

    def list_projects(self):

        self.ensure_workspace()

        return [

            p.name

            for p in self.ROOT.iterdir()

            if p.is_dir()

        ]

    def delete_project(self, name):

        shutil.rmtree(self.ROOT / name)

    def rename_project(self, old, new):

        (self.ROOT / old).rename(

            self.ROOT / new

        )