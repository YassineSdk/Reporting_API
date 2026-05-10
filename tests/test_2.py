from services.text_Validation import validate_text 
import pytest 
from fastapi import HTTPException


def test_success():

    report_input = {
    "report_description": "test test",
    "Recommendation_cmt": "test test",
    "Action_cmt": "test test test test",
    "footer_text": "test"}

    results = validate_text(report_input)
    assert results == report_input 
    

def test_failure():
    
    report_input = {
    "report_description": "t",
    "Recommendation_cmt": "y" * 851,
    "Action_cmt": "test test test test",
    "footer_text": "test"}

    with pytest.raises(HTTPException) as exc:

        validate_text(report_input)

        assert exc.value.status_code == 422

        assert "report_description" in exc.value.detail