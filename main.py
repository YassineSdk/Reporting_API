from fastapi import FastAPI, Form, UploadFile, File, Response , HTTPException 
from schemas.report_model import ReportModel
from fastapi.responses import FileResponse
import os 
from datetime import date
import json 
import logging
from typing import Annotated
import asyncio

from services.validation import Validate_data
from services.KPIs_calculation import get_KPIs
from services.logger_setup import setup_logging
from services.text_Validation import validate_text
from services.data_injection import injecting_data
from services.pdf_rendering import render_pdf

# logging config
setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title= "Reporting API",
    description="""This Service is responsable for generating a data driven report , informing 
                    management about the Perfomance of recommendation and actions implimentation
                """
                )


@app.get('/favicon.ico')
async def favicon():
    return Response(status_code=204)


@app.get('/')
def root():
    return {"Health checks":True}


@app.post('/Reporting_API')
async def Reporting_gen(
    report_description: Annotated[
            str,
            Form(description="Short description displayed under the report title"),
    ],
    Recommendation_cmt: Annotated[
            str,
            Form(description="Commentary for the recommendations section"),
    ],
    Action_cmt: Annotated[
            str,
            Form(description="Commentary for the actions section"),
    ],
    footer_text: Annotated[
            str,
            Form(description="Footer text displayed at the bottom of the report"),
    ],

    data:UploadFile = File(
        ...,
        description="CSV file"
        )
    ):


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

    ## Process

    # Data validation 
    data = Validate_data(content)

    # text input validation 
    validate_text(report_input)

    # Kpis calculation 
    recommed_KPis,RE_chart, action_KPIs,AS_chart,AE_chart = get_KPIs(data)

    #data injection 
    injecting_data(report_input,recommed_KPis,RE_chart, action_KPIs,AS_chart,AE_chart)

    #pdf rendering
    await asyncio.to_thread(
        render_pdf,
        "reports/preview.html",
        "reports/report.pdf"
    )
    

    file_path = "reports/report.pdf"
    file_name = f"report_{date.today()}"

    await asyncio.sleep(0.5)
    
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_name,
        headers={
        "Content-Disposition": "attachment; filename=report.pdf"
    }
    )
