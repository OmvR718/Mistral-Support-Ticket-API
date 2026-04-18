import json

from app.ai.embeddings.nomic_embedder import embed_query
from app.ai.retrieval.vector_search import retrieve_similar_chunks
from app.ai.prompts.classifier_prompt import build_classification_prompt
from app.ai.clients.ollama_client import run_classification


def classify_ticket_pipeline(db, ticket):
    
    # 1. Embed ticket
    embedding = embed_query(ticket.body)

    # 2. Retrieve relevant chunks
    chunks = retrieve_similar_chunks(db, embedding, top_k=5)

    # 3. Extract text only
    chunk_texts = [c.text for c in chunks]

    # 4. Build prompt
    prompt = build_classification_prompt(
        ticket_text=ticket.body,
        chunks=chunk_texts
    )

    # 5. Call LLM
    raw_output = run_classification(prompt)

    # 6. Parse JSON
    try:
        prediction = json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid LLM output: {raw_output}")

    # 7. Attach citations
    citations = [
        {
            "chunk_id": c.id,
            "doc_id": c.doc_id,
            "chunk_index": c.chunk_index
        }
        for c in chunks
    ]

    return {
        "category": prediction["category"],
        "priority": prediction["priority"],
        "confidence": prediction["confidence"],
        "citations": citations,
        "raw_output": raw_output
    }