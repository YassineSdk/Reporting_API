from fastapi import FastAPI, Query, UploadFile, File, Response , HTTPException ,Form
import uuid
from schemas.report_model import ReportModel,requestId
from fastapi.responses import FileResponse
from pathlib import Path
import os 
from datetime import date
import json 
import logging
from typing import Annotated
import asyncio
from pipeline import Pipeline
from services.logger_setup import setup_logging
from services.clear_storage import clear_storage
from contextlib import asynccontextmanager

# logging config
setup_logging()

logger = logging.getLogger(__name__)

# 
@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("App starting")

    #Check on evry startup 
    clear_storage()

    yield  

    logger.info(" app shutting down ...")


app = FastAPI(
    title= "Reporting API",
    lifespan=lifespan,
    description="""This Service is responsable for generating a data driven report , informing 
                    management about the Perfomance of recommendation and actions implimentation
                """
                )


@app.get('/')
def root():
    return {"Health checks":True}


@app.post('/report_gen')
async def Reporting_gen(
    report_description: Annotated[
            str,
            Form(description="Short description displayed under the report title",
            example="Rapport de suivi du premier trimestre 2024"),
        ],
    Recommendation_cmt: Annotated[
            str,
            Form(description="Commentary for the recommendations section",
            example="Les recommandations ont montré un taux d'acceptation de 85% au cours de cette période. Les actions correctives ont été mises en place pour les cas non acceptés."),
        ],
    Action_cmt: Annotated[
            str,
            Form(description="Commentary for the actions section",
            example="Les actions en cours représentent 60% du total avec un taux de mise en œuvre de 92% pour les actions critiques. Trois actions sont en retard et font l'objet d'un suivi renforcé."),
        ],
    footer_text: Annotated[
            str,
            Form(description="Footer text displayed at the bottom of the report",
            example="Rapport confidentiel - Tous droits réservés ONCF"),
        ],

    data:UploadFile = File(
        ...,
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

    

    file_path = f"{base_path}/report.pdf"
    file_name = f"report_{date.today()}"

    await asyncio.sleep(0.5)
    
    return {
        "request_id":request_id
    }

@app.get("/report/pdf")
async def get_report_pdf(
    requestId: str = Query(...,description="Request id")):

    base_path = f"storage/{requestId}"
    file_path = f"{base_path}/report.pdf"

    if not Path(file_path).exists():
        logger.error(f"the file does not exists in {file_path}")
        raise HTTPException(
            status_code=422,
            detail=f"the file does not exists in {file_path}"
        )

    file_name = f"report_{date.today()}"

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_name,
        headers={
        "Content-Disposition": "attachment; filename=report.pdf"
    }
    )

@app.get("/tables")
async def get_tables(
    requestId: str = Query(...,description="Request id")):

    logger.info(f"getting the aggrigation table for operation {requestId}")
    file_path = f"storage/{requestId}/tables.xls"

    if not Path(file_path).exists():
        logger.error(f" the file does not exist on location {file_path}")
        raise HTTPException(
            status_code=422,
            detail=f" the file does not exist on location {file_path} run the "
        )

    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"table{requestId}.xls"
        )




