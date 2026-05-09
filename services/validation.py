from fastapi import HTTPException
import pandas as pd 
from io import StringIO
import numpy as np
import logging


logger = logging.getLogger(__name__)

def Validate_data(content)-> pd.DataFrame:
    """
    this a data validation function it takes a content and turn it to a DataFrame 
    and check all this condiction :
    Process :
        1. Read file
        2. Transform -> DataFrame
        3. Validate dataframe not empty
        4. Validate required columns
        5. Validate column data types
        6. Validate allowed/expected values
        7. Validate nullable/non-nullable columns
    Output :
        A valid DataFrame object ready for aggregation

    """
    logger.info("Starting the data validation process")
    # Transforming the Csv to DataFrame

    try : 
        data = pd.read_csv(StringIO(content.decode("utf-8")))
    except Exception :
        logger.error("Failed to load the content file")
        raise HTTPException(
            status_code=422,
            detail="can't load the content file"
        )
    
    # Validating dataframe not empty 
    
    if data.empty :
        logger.error("Data is empty")
        raise HTTPException(
            status_code=422,
            details="the data is empty"
        )
    logger.info("Validating dataframe not empty : passed")
    
    EXPECTED_COLS = {
        'Mission_id':str,
        'N_Recommandation':str,
        'Recommandation':str,
        'Evaluation':str,
        'Recommendation_status':str,
        'Action_id':str,
        'Action':str,
        'Action_status':str
    }
    mandatory_cols = EXPECTED_COLS.keys()

    # checking the mandatory columns 
    
    missing_columns  = [
        col for col in mandatory_cols 
        if col not in data.columns
    ]

    if missing_columns:
        logger.error(f"Missing columns: {missing_columns}")
        raise HTTPException(
            status_code=422,
            detail = f"Missing columns {missing_columns}"
        )
    logger.info("checking the mandatory columns : passed")
    
    # validating the columns type 

    for col in mandatory_cols:
        if not data[col].dropna().map(type).eq(str).all():
            logger.error(f"Column {col} is expected to be a str")
            raise HTTPException(
                status_code=422,
                detail=f" column {col} is expected to be a str "
            )
    logger.info("validating the columns type : passed")

    # Validating the expected values

    EXPECTED_VALUES = {
        "Evaluation": ["Critique", "Modéré", "Mineur"],
        "Recommendation_status": ["accepté", "rejeté", "en etude"],
        "Action_status": ["En cours", "Non échues", "Clôturées",np.nan, "En continue", "En retard",'Rééchelonnées']
    }

    for col, allowed in EXPECTED_VALUES.items():
        invalid = ~data[col].isin(allowed)
        if invalid.any():
            logger.error(f"Invalid values in {col}: {data[col][invalid].unique().tolist()}")
            raise HTTPException(
                status_code=422,
                detail=f"Invalid values in {col}: {data[col][invalid].unique().tolist()}"
            )
    logger.info("Validating the expected values : Passed")
    
    # Validating the condition that None of this values could have NA or None or np.nan

    No_NA = ['Mission_id','N_Recommandation','Recommendation_status']

    for col in No_NA:
        if data[col].isna().any():
                logger.error(f"Column '{col}' cannot contain null values")
                raise HTTPException(
                status_code=422,
                detail=f"Column '{col}' cannot contain null values"
                )
    logger.info("Validating the None , Nan ,condition : Passed")

    return data
