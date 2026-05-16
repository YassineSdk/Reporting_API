from fastapi import FastAPI, Query, UploadFile, File, Response , HTTPException ,Form
import uuid
from pathlib import Path
from routes.report_gen import router as report_router
from routes.report_pdf import router as pdf_router
from routes.report_tables import router as tables_router
import os 
from datetime import date
import json 
import logging
import asyncio
from pipeline import Pipeline
from services.logger_setup import setup_logging
from services.clear_storage import clear_storage
from contextlib import asynccontextmanager
import time


# logging config
setup_logging()

logger = logging.getLogger(__name__)

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

app.include_router(report_router)
app.include_router(pdf_router)
app.include_router(tables_router)

@app.get('/')
def root():
    return {"Health checks" : True}



