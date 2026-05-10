from services.validation import Validate_data
from services.KPIs_calculation import get_KPIs
from services.text_Validation import validate_text
from services.data_injection import injecting_data
from services.pdf_rendering import render_pdf
from services.get_aggregates import get_aggregates
import asyncio


async def Pipeline(content,report_input,request_id):


    # Data validation 
    data = Validate_data(content)

    # text input validation 
    validate_text(report_input)

    # Kpis calculation 
    tables,recommed_KPis,RE_chart, action_KPIs,AS_chart,AE_chart = get_KPIs(data)

    #data injection 
    injecting_data(request_id,report_input,recommed_KPis,RE_chart, action_KPIs,AS_chart,AE_chart)

    #storing aggregation tables into excel workbook
    base_path = f"storage/{request_id}"

    # rendering pdf
    await asyncio.to_thread(
        render_pdf,
        f"{base_path}/preview.html",
        f"{base_path}/report.pdf"
    )
