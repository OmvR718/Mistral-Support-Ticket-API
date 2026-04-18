from ollama import embed

def embed_query(text:str)->list[float]:
    responese = embed(
        model="nomic-embed-text",
        input = text
        )
    return responese["embeddings"][0]
    