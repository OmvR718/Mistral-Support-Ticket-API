import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def run_classification(prompt: str, model: str = "mistral") -> str:

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]