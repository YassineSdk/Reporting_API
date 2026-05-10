from io import BytesIO
import pandas as pd 
import os
import logging
import xlsxwriter

logger = logging.getLogger(__name__)

def store_aggr(request_id,tables:dict ):
    """
        Writes a dict of DataFrames to an Excel buffer and saves the file to
    storage/<request_id>/.

    Args:
        tables:     {sheet_name: DataFrame} mapping.
        request_id: Used to build the output directory path.

    """
    logger.info("storing the aggregation tables ...")
    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        for sheetname, df in tables.items():
            df.to_excel(
                writer,
                sheet_name=sheetname,
                index=False
            )
    
    excel_buffer.seek(0)
    #storing the excelfile 
    base_path = f"storage/{request_id}"
    file_path = os.path.join(base_path,"tables.xls")
    with open(file_path,"wb") as f:
        f.write(excel_buffer.read())
    
    logger.info("storage of the aggregation tables : PASSED")
    







