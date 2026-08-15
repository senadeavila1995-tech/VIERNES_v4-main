import ast
from pathlib import Path


class ScannerAgent:

    IGNORE = {
        ".git",
        ".idea",
        ".vscode",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        "dist",
        "build",
        ".pytest_cache",
        ".mypy_cache"
    }

    def scan_project(self, root):

        root = Path(root)

        if not root.exists():
            raise Exception(f"No existe el proyecto: {root}")

        result = {
            "root": str(root),
            "folders": [],
            "files": [],
            "python": {},
            "summary": {
                "folders": 0,
                "files": 0,
                "python_files": 0,
                "classes": 0,
                "functions": 0
            }
        }

        for path in root.rglob("*"):

            if any(i in path.parts for i in self.IGNORE):
                continue

            if path.is_dir():

                result["folders"].append(str(path))

                continue

            result["files"].append(str(path))

            if path.suffix == ".py":

                info = self.scan_python(path)

                result["python"][str(path)] = info

                result["summary"]["python_files"] += 1
                result["summary"]["classes"] += len(info["classes"])
                result["summary"]["functions"] += len(info["functions"])

        result["summary"]["folders"] = len(result["folders"])
        result["summary"]["files"] = len(result["files"])

        return result

    def scan_python(self, file):

        try:

            source = Path(file).read_text(
                encoding="utf8",
                errors="ignore"
            )

            tree = ast.parse(source)

        except Exception:

            return {

                "classes": [],
                "functions": [],
                "imports": []

            }

        classes = []
        functions = []
        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                classes.append(node.name)

            elif isinstance(node, ast.FunctionDef):

                functions.append(node.name)

            elif isinstance(node, ast.Import):

                for imp in node.names:

                    imports.append(imp.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:

                    imports.append(node.module)

        return {

            "classes": classes,

            "functions": functions,

            "imports": imports

        }