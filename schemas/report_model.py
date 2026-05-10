from pydantic import BaseModel ,Field


class ReportModel(BaseModel):
    report_description: str 
    Recommendation_cmt : str
    Action_cmt : str
    footer_text : str 

class requestId(BaseModel):
    request_id : str 
