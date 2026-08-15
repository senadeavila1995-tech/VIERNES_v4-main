from pathlib import Path
import shutil

from agents.crud.models.generation_context import GenerationContext


class FrameworkInstaller:
    """
    Instala y sincroniza el framework base dentro del proyecto generado.

    La instalación ocurre una sola vez por generación, pero los archivos
    faltantes del framework se sincronizan incluso si el directorio destino
    ya existe.
    """

    METADATA_KEY = "framework_installed"

    # ==========================================================
    # Instalación
    # ==========================================================

    def install(
        self,
        context: GenerationContext,
    ) -> None:

        source = self._framework_source()

        destination = (
            Path(context.project.source_path)
            / "backend"
            / "framework"
        )

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ------------------------------------------------------
        # Sincronizar framework
        # ------------------------------------------------------

        shutil.copytree(
            source,
            destination,
            dirs_exist_ok=True,
        )

        print("\n========== FRAMEWORK ==========")
        print("Origen :", source)
        print("Destino:", destination)
        print("Existe :", destination.exists())
        print("===============================\n")

        context.set_metadata(
            self.METADATA_KEY,
            True,
        )

    # ==========================================================
    # Framework origen
    # ==========================================================

    def _framework_source(self) -> Path:

        return Path(__file__).resolve().parents[2] / "framework"
