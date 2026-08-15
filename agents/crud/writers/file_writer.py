from pathlib import Path

from agents.crud.installers.framework_installer import FrameworkInstaller
from agents.crud.installers.frontend_installer import FrontendInstaller
from agents.crud.models.generated_file import GeneratedFile
from agents.crud.models.generation_context import GenerationContext
from agents.crud.resolvers.folder_resolver import FolderResolver
from agents.crud.resolvers.path_resolver import PathResolver


class FileWriter:
    """
    Responsable de persistir los archivos generados.

    Responsabilidades:

    - Instalar la estructura base del proyecto.
    - Crear la estructura del módulo.
    - Escribir GeneratedFile.

    No genera contenido.
    No resuelve nombres.
    """

    def __init__(self):

        self.framework_installer = FrameworkInstaller()

        self.frontend_installer = FrontendInstaller()

    # ==========================================================
    # Escritura múltiple
    # ==========================================================

    def write_all(
        self,
        generated_files: list[GeneratedFile],
        context: GenerationContext,
    ) -> list[Path]:
        """
        Escribe todos los archivos generados.
        """

        paths: list[Path] = []

        # Instalar framework backend (una sola vez)
        self.framework_installer.install(context)

        # Instalar frontend React/Vite (una sola vez)
        self.frontend_installer.install(context)

        # Crear estructura del módulo (una sola vez)
        FolderResolver.create_entity_structure(
            context.project.source_path,
            context.entity_name,
        )

        for generated_file in generated_files:

            path = self.write(
                generated_file,
                context,
            )

            paths.append(path)

        return paths

    # ==========================================================
    # Escritura individual
    # ==========================================================

    def write(
        self,
        generated_file: GeneratedFile,
        context: GenerationContext,
    ) -> Path:
        """
        Escribe un único archivo generado.
        """

        path = PathResolver.build(
            output_dir=context.project.source_path,
            layer=generated_file.layer,
            entity=generated_file.entity,
            folder=generated_file.folder,
            filename=generated_file.filename,
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if path.exists() and not generated_file.overwrite:

            print(f"⚠ Se omitió {path}")

            return path

        path.write_text(
            generated_file.content,
            encoding=generated_file.encoding,
        )

        print(f"✓ {generated_file}")

        return path
