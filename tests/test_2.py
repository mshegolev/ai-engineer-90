from pydantic import ValidationError
import pytest


from src.models.jira_ticket import JiraTicket


def test_priority_below_minimum():
    """
    Требования:
    - Передай priority=0.
    - Используй pytest.raises(ValidationError).
    - Проверь, что ошибка относится к полю priority.
    - Проверь, что тип ошибки — greater_than_equal.
    """
    with pytest.raises(ValidationError) as inf_exc:
        JiraTicket(ticket_id="DATA-12345",
                    summary="My net test ticket for jiraticket validation",
                    priority=0,
                    confidence=0.5,
                    test_type="unit")
    errors = inf_exc.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("priority",)
    assert errors[0]["type"] == "greater_than_equal"
    assert errors[0]["input"] == 0
    error_ctx = errors[0].get('ctx', {})
    assert error_ctx["ge"] == 1 

