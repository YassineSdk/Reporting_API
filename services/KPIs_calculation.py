import pandas as pd 
import numpy as numpy
import logging
from datetime import date


logger = logging.getLogger(__name__)

def get_KPIs(data:pd.DataFrame)-> dict:
    """
    this is the aggregation function that calculates Performance KPis
    related to recommendations and actions implimentation

    input : 
        data : DataFrame columns
    
    output : in order 
            recommed_KPis = {}   stores recomendation KPIs
            RE_chart = {}        recommendation by evaluation
            action_KPIs = {}     stores the actions KPIs
            AS_chart = {}        actions by status
            AE_chart = {}        actions by evaluation

    """
    logger.info('starting the Kpi calculation')

    recommed_KPis = {} #stores recomendation kPIS
    action_KPIs = {}
    RE_chart = {} # recommendation by evaluation
    AS_chart = {} # actions by status
    AE_chart = {} # actions by evaluation

    # data preprocessing :
    #-- converting date column into datetime type 
    data['Échéance'] = pd.to_datetime(data['Échéance'],format="%Y-%m-%d")

    # Recommendation summary columns [Mission_id,Nb_accepté,Nb_rejeté, Nb_en etude, total_recommendation] 
    agg_dict = {
    f"Nb_{status}": (
        "N_Recommandation",
        lambda x, status=status: x[data.loc[x.index, "Recommendation_status"] == status ].nunique()
    )
    for status in data["Recommendation_status"].unique()
    }

    agg_dict["total_recommendation"] = (
        "N_Recommandation",
        "nunique"
    )

    tableau_1 = (
        data.groupby("Mission_id")
        .agg(**agg_dict)
        .reset_index()
    )
    recommed_KPis["Total_recom"] = tableau_1["total_recommendation"].sum().item()
    recommed_KPis["Total_recom_ACC"] = tableau_1["Nb_accepté"].sum().item()
    recommed_KPis["Total_recom_Rej"] = tableau_1["Nb_rejeté"].sum().item()
    recommed_KPis["Total_recom_etu"] = tableau_1["Nb_en etude"].sum().item()
    recommed_KPis["acceptation_rate"] = (round(recommed_KPis["Total_recom_ACC"]/recommed_KPis["Total_recom"],2)*100)


    # accepted recommendations count by Evaluation
    tableau_2 = (
    data.loc[data['Recommendation_status'] == "accepté",["N_Recommandation","Evaluation"]]
    .groupby("Evaluation")
    .agg(nb_recomendation=("N_Recommandation","nunique"))
    .reset_index())
    RE_chart = tableau_2.set_index("Evaluation")["nb_recomendation"].to_dict()


    # Actions count  by status 
    tableau_3 = (
    data[['Action_id',"Action_status"]].dropna()
    .groupby("Action_status")
    .agg(nb_action=("Action_id","nunique"))
    .reset_index()
        )
    AS_chart = tableau_3.set_index("Action_status")["nb_action"].to_dict()


    # Actions count by evaluation
    tableau_4 = (
    data[["Action_id","Evaluation"]]
    .groupby("Evaluation")
    .agg(nb_action=("Action_id","nunique"))
    .reset_index()
    )
    AE_chart = tableau_4.set_index("Evaluation")["nb_action"].to_dict()


    # Taux de mise en œuvre des actions : T1
    d = tableau_3.set_index("Action_status")["nb_action"].to_dict()
    action_echues = (
        data.loc[data["Échéance"] <= pd.Timestamp.today()]['Action_id']
        .nunique())

    T1 = round((d["En continue"] + d["Clôturées"]) / (action_echues + d["En continue"]) ,2) *100


    # Taux de mise en œuvre des actions critiques : T2
    # ACR : Action Crtitique Realisé
    ACR = data[
        (data["Evaluation"] == "Critique") & 
        (
            (data["Action_status"] == "Clôturées") |
            (data["Action_status"] == "En cours")
        )
        ]['Action_id'].nunique()

    nb_action_critique = tableau_4.loc[tableau_4["Evaluation"] =="Critique"]['nb_action'].item()
    T2 = round( ACR / nb_action_critique,2) * 100
    
    action_KPIs['total_actions'] = tableau_3['nb_action'].sum().item()
    action_KPIs["T1"] = T1
    action_KPIs["T2"] = T2


    logger.info('Kpi calculated successfully')
    tables = {
            "full_data":data,
            "recommendation_aggr":tableau_1,
            "recomendation_status":tableau_2,
            "actions_status":tableau_3,
            "actions_evaluation":tableau_4
            }

    return tables, recommed_KPis,RE_chart, action_KPIs,AS_chart,AE_chart



## test
# data = pd.read_csv("mock_data.csv")
# recommed_KPis,RE_chart, action_KPIs,AS_chart,AE_chart = get_KPIs(data)

# print("recommendation_kpis")
# print(recommed_KPis)
# print("recommendation pie chart")
# print(RE_chart)
# print("actions Kpis")
# print(action_KPIs)
# print("actions barchart")
# print(AS_chart)
# print("actions Piechart")
# print(AE_chart)


