from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_database
from app.db.models import Ticket
from app.ai.pipelines.classify_ticket import classify_ticket_pipeline
from app.db.crud.ticket_pred_crud import create_prediction
from app.db.crud.logs_crud import create_log

router = APIRouter()

@router.post("/tickets/{id}/classify")
def classify_ticket(id: int, db: Session = Depends(get_database)):

    # 1. Fetch ticket
    ticket = db.query(Ticket).filter(Ticket.id == id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # 2. Run AI pipeline
    result = classify_ticket_pipeline(db, ticket)

    # 3. Store prediction
    prediction = create_prediction(
        db=db,
        ticket_id=id,
        category=result["category"],
        priority=result["priority"],
        confidence=result["confidence"]
    )

    # 4. Store log
    create_log(
        db=db,
        ticket_id=id,
        prompt=result.get("prompt", ""),
        response=result["raw_output"],
        citations=result["citations"],
        model_name="mistral"
    )

    # 5. Return response
    return {
        "ticket_id": id,
        "prediction": {
            "category": prediction.category,
            "priority": prediction.priority,
            "confidence": prediction.confidence
        },
        "citations": result["citations"]
    }