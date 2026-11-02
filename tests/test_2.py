from unittest.mock import Mock

from pydantic import ValidationError
import pytest

from src.models.jira_ticket import JiraTicket, validate_with_retry


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

    error = errors[0]

    assert error["loc"] == ("priority",)
    assert error["type"] == "greater_than_equal"
    assert error["input"] == 0

    ctx = error.get("ctx")
    assert ctx is not None
    assert ctx["ge"] == 1




def test_retry_stops_after_success():
    generator = Mock(side_effect=[
        {
            "ticket_id": "DATA-12345",
            "summary": "Verify ETL pipeline",
            "priority": 10,
            "confidence": 0.9,
            "test_type": "unit",
        },
        {
            "ticket_id": "DATA-12345",
            "summary": "Verify ETL pipeline",
            "priority": 3,
            "confidence": 0.9,
            "test_type": "unit",
        },
    ])

    result = validate_with_retry(
        generator,
        max_attempts=3,
    )
    assert result['process_status'] == 'COMPLETED'
    assert result["ticket"]["data"]["priority"] == 3
    
    assert result['attempts'] == 2
    assert generator.call_count == 2


def test_zero_attempts_must_raise_value_error():
    generator = Mock()

    with pytest.raises(ValueError):
        validate_with_retry(generator, max_attempts=0)

    generator.assert_not_called()
