def build_classification_prompt(ticket_text: str, chunks: list[str]) -> str:

    context = "\n\n".join(chunks) if chunks else "No knowledge available."

    return f"""
You are a strict support ticket classifier.

Use ONLY the allowed labels below.

CATEGORY (choose one):
- billing_issue
- technical_support
- account_issue
- feature_request
- general_inquiry

PRIORITY (choose one):
- low
- medium
- high
- urgent

Knowledge context:
{context}

Ticket:
{ticket_text}

Return ONLY valid JSON:
{{
  "category": "...",
  "priority": "...",
  "confidence": 0.0
}}
"""