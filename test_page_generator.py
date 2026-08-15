from agents.crud.generators.frontend.page_generator import PageGenerator


class Context:
    entity_name = "Producto"


generator = PageGenerator()

result = generator.generate(Context())

print(result.relative_path)
print(result.content)
