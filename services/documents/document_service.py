from pathlib import Path


class DocumentService:

    def create(self, path):

        file = Path(path)

        file.parent.mkdir(parents=True, exist_ok=True)

        file.touch(exist_ok=True)

        return file

    def exists(self, path):

        return Path(path).exists()

    def read(self, path):

        file = Path(path)

        if not file.exists():
            return ""

        return file.read_text(encoding="utf-8")

    def write(self, path, text):

        Path(path).write_text(
            text,
            encoding="utf-8"
        )

    def append(self, path, text):

        with open(path, "a", encoding="utf-8") as file:

            file.write(text)

    def insert_line(self, path, line, text):

        file = Path(path)

        lines = []

        if file.exists():

            lines = file.read_text(
                encoding="utf-8"
            ).splitlines()

        while len(lines) < line:
            lines.append("")

        lines.insert(line, text)

        file.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )

    def replace(self, path, old, new):

        content = self.read(path)

        content = content.replace(old, new)

        self.write(path, content)