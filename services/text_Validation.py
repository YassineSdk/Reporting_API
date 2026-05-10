from fastapi import HTTPException 
import logging 


logger = logging.getLogger(__name__)

def validate_text(report_input:dict):
    """
    Validate the text data lenght by checking if the condition stored in 
    the condition dict is less than the lenght of text 
    input :
        report_input (dict) :stores the text passed by the user 
    output : 
        report_input (dict) : returns the same dict of the condition is verified for all the items of the dict
    """
    conditions = {
    "report_description": 200,
    "Recommendation_cmt": 850,
    "Action_cmt": 900,
    "footer_text": 150}

    logger.info('started the text validation ')

    for key ,max_len in conditions.items():

        value = report_input[key]
        if value is not None and len(value) > max_len:
        
            logger.error(f"{key} can't have more than {max_len} characters")

            raise HTTPException(
                status_code=422,
                detail=f"{key} can't have more than {max_len} characters"
            )

    logger.info('started the text validation : PASSED')

    

    