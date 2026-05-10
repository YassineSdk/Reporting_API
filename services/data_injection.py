from jinja2 import Environment, FileSystemLoader
from fastapi import HTTPException
import os 
import logging

from datetime import date

logger =  logging.getLogger(__name__)


def injecting_data(request_id,report_input,recommed_KPis,RE_chart, action_KPIs,AS_chart,AE_chart):
    """
    """

    logger.info("Started data injection")

    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('report_template.html')

    if not template:
        logger.error('the report template is empty')
        raise HTTPException(
            status_code=422,
            detail="the report template is empty"
        )
    
    objects_to_check = [
    report_input,
    recommed_KPis,
    RE_chart,
    action_KPIs,
    AS_chart,
    AE_chart ]

    if any(not obj for obj in objects_to_check):
        logger.error(f'the {obj} dict is empty')
        raise HTTPException(
            status_code=422,
            detail=f"the {obj} dict is empty"
        )



    html_report = template.render(    
    report_date=date.today(),
    total_recommendations=recommed_KPis['Total_recom'],
    recommendations_accepted=recommed_KPis['Total_recom_ACC'],
    recommendations_not_accepted=recommed_KPis['Total_recom_Rej'],
    recommendations_under_study=recommed_KPis['Total_recom_etu'],
    acceptance_rate=int(recommed_KPis['acceptation_rate']),
    total_actions=action_KPIs['total_actions'],
    actions_implementation_rate=int(action_KPIs['T1']),
    critical_actions_implementation_rate=int(action_KPIs['T2']),
    chart_s1_critique=RE_chart['Critique'],
    chart_s1_modere=RE_chart['Modéré'],
    chart_s1_mineur=RE_chart['Mineur'],
    chart_s2_non_echues=AS_chart['Non échues'],
    chart_s2_en_cours=AS_chart['En cours'],
    chart_s2_cloture=AS_chart['Clôturées'],
    chart_s2_en_retard=AS_chart['En retard'],
    chart_s2_reechelonne=AS_chart['Rééchelonnées'],
    chart_pie_critique=AE_chart['Critique'],
    chart_pie_modere=AE_chart['Modéré'],
    chart_pie_mineur=AE_chart['Mineur'],
    # text variables...
    report_description=report_input["report_description"],
    section1_text_p1=report_input["Recommendation_cmt"],
    section2_text_p1=report_input["Action_cmt"],
    footer_text=report_input["footer_text"]
    )

    base_path = f"storage/{request_id}"
    with open(f'{base_path}/preview.html', 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    logger.info("Data injected successfull")



