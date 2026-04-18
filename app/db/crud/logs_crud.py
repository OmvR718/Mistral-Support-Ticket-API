from sqlalchemy.orm import Session
from app.db.models import Log


def create_log(
    db: Session,
    ticket_id: int,
    prompt: str,
    response: str,
    citations: list[dict],
    model_name: str = "mistral",
    user_id: int | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    action: str = "classify"
) -> Log:

    log = Log(
        ticket_id=ticket_id,
        user_id=user_id,
        action=action,
        prompt=prompt,
        response=response,
        citations=citations,
        model_name=model_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log

def get_logs_by_ticket(
    db: Session,
    ticket_id: int,
    limit: int = 20
) -> list[Log]:

    return (
        db.query(Log)
        .filter(Log.ticket_id == ticket_id)
        .order_by(Log.created_at.desc())
        .limit(limit)
        .all()
    )