from agents.crud.models.generation_context import GenerationContext
from agents.crud.registry.generator_registry import GeneratorRegistry
from agents.crud.writers.file_writer import FileWriter
from agents.crud.resolvers.relationship_resolver import RelationshipResolver


class CrudGenerator:
    """
    Orquesta la generación completa del CRUD.

    Flujo:

    Generator
          ↓
    GeneratedFile / list[GeneratedFile]
          ↓
    FileWriter
          ↓
    Archivo físico
    """

    def __init__(self):
        self.registry = GeneratorRegistry()
        self.writer = FileWriter()

    # ==========================================================
    # Generar CRUD
    # ==========================================================

    def generate(
        self,
        context: GenerationContext,
    ):

        # ======================================================
        # Resolver relaciones ORM antes de generar modelos
        # ======================================================

        generators = sorted(
            self.registry.all(),
            key=lambda generator: generator.order,
        )

        RelationshipResolver.resolve(
            context.definitions
        )


        print("\n========== DEBUG DEFINITIONS AFTER RESOLVE ==========")

        for name, definition in context.definitions.items():

            print(
                name,
                "fields=",
                len(definition.fields),
                "relations=",
                len(definition.relationships)
            )

            for relation in definition.relationships:

                print(
                    "   ",
                    relation.name,
                    "->",
                    relation.target,
                    "back=",
                    relation.back_populates
                )

        print("=====================================================\n")


        generated_files = []

        # ======================================================
        # Generar entidades relacionadas completas
        # ======================================================
        #
        # Si una entidad relacionada participa en una relación,
        # debe generarse como CRUD completo y no solamente el modelo.
        #
        # Ejemplo:
        #
        # Pedido.creado_por_id -> Usuario
        #
        # Usuario necesita:
        # model
        # schemas
        # dto
        # repository
        # service
        # controller
        # routes
        #
        
        current_definition = context.definition


        for entity_name, definition in context.definitions.items():

            if entity_name == context.entity_name:
                continue


            if not definition.relationships:
                continue


            context.definition = definition


            for generator in generators:

                if generator.name in [
                    "main",
                    "root_routes",
                ]:
                    continue


                if not generator.validate(context):
                    continue


                generated = generator.generate(
                    context
                )


                if generated is None:
                    continue


                if isinstance(generated, list):

                    generated_files.extend(
                        generated
                    )

                else:

                    generated_files.append(
                        generated
                    )


        context.definition = current_definition


        for generator in generators:

            if generator.name in [
                "main",
                "root_routes",
            ]:
                continue

            if not generator.validate(context):
                continue

            generated = generator.generate(context)

            if generated is None:
                continue

            # Un generador normal devuelve GeneratedFile.
            if isinstance(generated, list):

                generated_files.extend(generated)

            else:

                generated_files.append(generated)


        # ======================================================
        # GENERADORES RAÍZ DEL PROYECTO
        # ======================================================

        print("DEBUG ROOT CONTEXT")
        print("DEFINITIONS:", context.definitions)

        for generator in generators:

            if generator.name not in [
                "main",
                "root_routes",
            ]:
                continue

            if not generator.validate(context):
                continue

            generated = generator.generate(context)

            if generated is None:
                continue

            if isinstance(generated, list):

                generated_files.extend(generated)

            else:

                generated_files.append(generated)

        paths = self.writer.write_all(
            generated_files,
            context,
        )

        for path in paths:
            context.add_generated_file(str(path))

        return paths
