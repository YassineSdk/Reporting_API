import logging 
from playwright.sync_api import sync_playwright
from pathlib import Path
import os
from fastapi import HTTPException

logger = logging.getLogger(__name__)

def render_pdf(html_path, output_path):

    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / html_path

    if not file_path.exists():
        logger.error(f"The file does not exists {file_path}")
        raise HTTPException(
            status_code=422,
            detail= f"The file does not exists {file_path}"
        )


    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        
        context = browser.new_context(
            viewport={"width": 1200, "height": 1600},
            #device_scale_factor=2,  
        )
        
        page = context.new_page()
        abs_path = os.path.abspath(html_path)
        page.goto(f"file:///{abs_path}", wait_until="networkidle")
        page.wait_for_timeout(1500)
        
        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        
        browser.close()


## test
# render_pdf("reports/preview.html","reports/report.pdf") 
