def build_classification_prompt(ticket_text: str, chunks: list[str]) -> str:

    context = "\n\n".join(chunks)

    prompt = f"""
You are a support ticket classifier.

Use ONLY the provided knowledge context.

Knowledge:
{context}

Task:
Classify the ticket into:
- category
- priority
- confidence (0 to 1)

Return ONLY valid JSON:
{{
  "category": "...",
  "priority": "...",
  "confidence": 0.0
}}

Ticket:
{ticket_text}
"""

    return prompt