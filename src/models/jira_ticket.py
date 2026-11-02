from pydantic import BaseModel, Field, ValidationError
from typing import Literal


class JiraTicket(BaseModel):
    """
    Class for validate Jira ticket
    """

    ticket_id: str = Field(min_length=5)
    summary: str = Field(min_length=10)
    priority: int = Field(ge=1, le=5)
    confidence: float = Field(ge=0, le=1)
    test_type: Literal["unit", "integration", "e2e"]


def validate_ticket(data: dict) -> dict:
    try:
        ticket = JiraTicket.model_validate(data)

        return {
            "status": "valid",
            "data": ticket.model_dump(),
            "errors": [],
        }

    except ValidationError as exc:
        errors = []

        for error in exc.errors():
            errors.append({
                "field": ".".join(map(str, error["loc"])),
                "code": error["type"],
                "message": error["msg"],
            })

        return {
            "status": "invalid",
            "data": None,
            "errors": errors,
        }

def validate_with_retry(generate, max_attempts=3):
    """  
        # Здесь нужно проверить данные
        # Если данные корректны — вернуть COMPLETED
        # Если нет — перейти к следующей попытке
    """
    attempt = 0
    for attempt in range(1,max_attempts+1,1):
        data = generate()
        ticket  = validate_ticket(data=data)
        if ticket['status'] == 'valid':
            return {'process_status':'COMPLETED',
                "attempts": attempt,
             'ticket':ticket}
    return {"process_status": "WAITING_FOR_HUMAN",
                "attempts": attempt,
             'ticket':ticket}

def generate_invalid_ticket():
    return {
        "ticket_id": "DATA-12345",
        "summary": "Verify ETL pipeline",
        "priority": 10,
        "confidence": 0.9,
        "test_type": "unit",
    }
result = validate_with_retry(
    generate_invalid_ticket,
    max_attempts=3,
)

print(result)
