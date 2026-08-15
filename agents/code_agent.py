from pathlib import Path
import shutil


class CodeAgent:

    def __init__(self):

        self.backup_folder = Path("memory/backups")

        self.backup_folder.mkdir(
            parents=True,
            exist_ok=True
        )


    # ==================================================
    # LECTURA
    # ==================================================

    def read_file(self, path):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        )


    # ==================================================
    # ESCRITURA
    # ==================================================

    def write_file(self, path, content):

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            content,
            encoding="utf-8"
        )

        return str(path)


    # ==================================================
    # APPEND
    # ==================================================

    def append_file(self, path, text):

        path = Path(path)

        with open(
            path,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(text)

        return True


    # ==================================================
    # BACKUP
    # ==================================================

    def backup(self, path):

        path = Path(path)

        if not path.exists():
            return False

        backup = self.backup_folder / path.name

        shutil.copy2(
            path,
            backup
        )

        return True


    # ==================================================
    # RESTAURAR
    # ==================================================

    def restore(self, filename):

        backup = self.backup_folder / filename

        if not backup.exists():
            return False

        shutil.copy2(
            backup,
            filename
        )

        return True


    # ==================================================
    # REEMPLAZAR TEXTO
    # ==================================================

    def replace_text(
        self,
        path,
        old,
        new
    ):

        content = self.read_file(path)

        self.backup(path)

        content = content.replace(
            old,
            new
        )

        self.write_file(
            path,
            content
        )

        return True


    # ==================================================
    # INSERTAR
    # ==================================================

    def insert_after(
        self,
        path,
        marker,
        text
    ):

        content = self.read_file(path)

        if marker not in content:
            return False

        self.backup(path)

        content = content.replace(
            marker,
            marker + "\n" + text
        )

        self.write_file(
            path,
            content
        )

        return True


    # ==================================================
    # BUSCAR
    # ==================================================

    def find_text(
        self,
        path,
        text
    ):

        content = self.read_file(path)

        return text in content


    # ==================================================
    # ELIMINAR
    # ==================================================

    def delete_file(self, path):

        path = Path(path)

        if path.exists():

            path.unlink()

            return True

        return False


    # ==================================================
    # CARPETAS
    # ==================================================

    def create_folder(self, path):

        Path(path).mkdir(
            parents=True,
            exist_ok=True
        )


    # ==================================================
    # LISTAR
    # ==================================================

    def list_files(self, root):

        root = Path(root)

        return [

            str(file)

            for file in root.rglob("*")

            if file.is_file()

        ]


    # ==================================================
    # GENERAR ARCHIVO CON IA
    # ==================================================

    def generate_file(
        self,
        prompt,
        llm
    ):

        return llm.generate_code(prompt)


    # ==================================================
    # CORREGIR CÓDIGO
    # ==================================================

    def fix_code(
        self,
        file,
        llm,
        error
    ):

        source = self.read_file(file)

        prompt = f"""

Eres un desarrollador Senior.

Corrige el siguiente código.

Devuelve únicamente el código completo.


ERROR:

{error}


CÓDIGO:

{source}

"""


        new_code = llm.generate_code(prompt)

        self.backup(file)

        self.write_file(
            file,
            new_code
        )

        return True