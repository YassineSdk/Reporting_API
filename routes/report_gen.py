from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Annotated
from schemas.report_model import ReportModel
import asyncio
import uuid
import os
import logging
from pipeline import Pipeline 

logger = logging.getLogger(__name__)
router = APIRouter(tags=['Report Generation']) 

@router.post("/report_gen")
async def Reporting_gen(
    report_description: Annotated[str,Form(...,description="Short description displayed under the report title")],
    Recommendation_cmt: Annotated[
            str,
            Form(...,description="Commentary for the recommendations section")],
    Action_cmt: Annotated[
            str,
            Form(...,description="Commentary for the actions section")],
    footer_text: Annotated[
            str,
            Form(...,description="Footer text displayed at the bottom of the report")],

    data:UploadFile = File(...,
        description="CSV file containing the data for the report"
        )
    ):


    # getting request_id
    request_id = uuid.uuid4().hex[:6]

    ALLOWED_TYPES = ["text/csv","application/vnd.ms-excel"]

    print(data.content_type)

    # Validating the type file
    if data.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only csv files are allowed"
        )
    
    logger.info(" the filetype is valid")

    # Creating the request model
    text_input = ReportModel(
        report_description=report_description,
        Recommendation_cmt=Recommendation_cmt,
        Action_cmt=Action_cmt,
        footer_text=footer_text,
    )

    report_input = text_input.model_dump()

    # Read Csv file 
    content = await data.read()

    # create folder
    base_path = f"storage/{request_id}"
    os.makedirs(base_path,exist_ok=True)


    ## Process
    await Pipeline(content,report_input,request_id)
    

    return {
        "request_id":request_id
    } 
