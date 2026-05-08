from pydantic import BaseModel 


class ReportModel(BaseModel):
    report_description: str 
    Recommendation_cmt : str
    Action_cmt : str
    footer_text : str 


