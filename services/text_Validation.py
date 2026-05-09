from fastapi import HTTPException 
import logging 


logger = logging.getLogger(__name__)

def text_validation(report_input:dict):
    """

    """
    conditions = {
    "report_description": 200,
    "Recommendation_cmt": 850,
    "Action_cmt": 900,
    "footer_text": 150}

    for key in report_input.keys():
        if len(report_input[key]) > conditions[key] :
            logger.error(f"this text can't have more than {conditions[key]} charater")
            raise HTTPException(
                status_code=422,
                detail=f"this text can't have more than {conditions[key]} charater"
            )

    return report_input

