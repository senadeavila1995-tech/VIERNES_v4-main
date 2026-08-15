from agents.assistant_agent import AssistantAgent

assistant = AssistantAgent()

print("=" * 50)
print("🤖 VIERNES v4")
print("=" * 50)

while True:

    text = input("\nTÚ > ")

    if text.lower() in ["salir", "exit"]:
        break

    response = assistant.process(text)

    print(f"\nVIERNES > {response}")