import subprocess
from pathlib import Path


class TerminalAgent:

    def run(
        self,
        command,
        cwd=None,
        timeout=300
    ):

        try:

            result = subprocess.run(

                command,

                cwd=cwd,

                shell=True,

                capture_output=True,

                text=True,

                timeout=timeout

            )

            return {

                "success": result.returncode == 0,

                "return_code": result.returncode,

                "stdout": result.stdout,

                "stderr": result.stderr

            }

        except subprocess.TimeoutExpired:

            return {

                "success": False,

                "stdout": "",

                "stderr": "Tiempo agotado."

            }

        except Exception as e:

            return {

                "success": False,

                "stdout": "",

                "stderr": str(e)

            }

    # ================================================

    def run_python(

        self,

        script,

        cwd=None

    ):

        return self.run(

            f'python "{script}"',

            cwd=cwd

        )

    # ================================================

    def run_pip(

        self,

        command,

        cwd=None

    ):

        return self.run(

            f"pip {command}",

            cwd=cwd

        )

    # ================================================

    def run_git(

        self,

        command,

        cwd=None

    ):

        return self.run(

            f"git {command}",

            cwd=cwd

        )

    # ================================================

    def run_npm(

        self,

        command,

        cwd=None

    ):

        return self.run(

            f"npm {command}",

            cwd=cwd

        )

    # ================================================

    def run_pytest(

        self,

        cwd=None

    ):

        return self.run(

            "pytest",

            cwd=cwd

        )