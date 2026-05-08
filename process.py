# generate_report.py
from jinja2 import Environment, FileSystemLoader
import os 
from playwright.sync_api import sync_playwright
from pathlib import Path

env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('report_template.html')

html_output = template.render(

    report_date='06 mai 2026',
    total_recommendations=48,
    recommendations_accepted=25,
    recommendations_not_accepted=10,
    recommendations_under_study=15,
    acceptance_rate='70',
    total_actions=50,
    actions_implementation_rate='42',
    critical_actions_implementation_rate='36',
    chart_s1_critique=10,
    chart_s1_modere=5,
    chart_s1_mineur=12,
    chart_s2_non_echues=10,
    chart_s2_en_cours=14,
    chart_s2_cloture=6,
    chart_s2_en_retard=8,
    chart_s2_reechelonne=10,
    chart_pie_critique=37,
    chart_pie_modere=18.5,
    chart_pie_mineur=44.4,
    # text variables...
    report_description='Suivi trimestriel des recommandations d\'audit',
    section1_text_p1='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
    section1_text_p2='Deuxième paragraphe avec plus de détails...',
    section2_text_p1='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
    section2_text_p2='Suivi des actions critiques...',
    footer_text='Document confidentiel - ONCF 2026'
)

# Save the file
with open('reports/preview.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print("Report generated: preview.html")
print("Double-click preview.html to open in your browser")

from playwright.sync_api import sync_playwright
from pathlib import Path

def html_to_pdf(html_path, output_path):
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

html_to_pdf("reports/preview.html","reports/report.pdf")
