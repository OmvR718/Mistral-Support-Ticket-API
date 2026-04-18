import ollama
import random

def embed_query(text:str)->list[float]:
    """
    Generate embeddings for text using Ollama
    Falls back to mock embeddings if Ollama is not available
    """
    try:
        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=text
            )
        return response["embedding"]
    except Exception as e:
        # Fallback to mock embeddings for testing
        print(f"Warning: Ollama not available, using mock embeddings. Error: {e}")
        # Generate consistent mock embeddings based on text hash
        seed = hash(text) % 10000
        random.seed(seed)
        return [random.uniform(-1, 1) for _ in range(768)]