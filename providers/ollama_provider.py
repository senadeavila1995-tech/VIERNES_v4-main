import requests


class OllamaProvider:

    def __init__(self):

        self.url = "http://localhost:11434/api/chat"

        self.model = "llama3.2:latest"

    def ask(self, prompt):

        if not isinstance(prompt, list):

            prompt = [{"role": "user", "content": prompt}]

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.1},
            },
        )

        if response.status_code != 200:

            raise Exception(response.text)

        data = response.json()

        if "message" not in data:

            raise Exception(f"Respuesta inválida Ollama: {data}")

        return data["message"]["content"]
