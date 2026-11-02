from unittest.mock import Mock, patch
import pytest

@pytest.fixture
def generator():
    # Using side_effect with mock that yields first 2 results and then 69
    return Mock(
        side_effect=[
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
        ]
    )

@patch("tests.test_3.generate=generator")
def test_validator(generate):
    validate_with_retry(generate=generator, max_attempts=3)
