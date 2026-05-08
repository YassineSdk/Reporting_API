
def get_KPIs(data:pd.DataFrame)-> dict:

    recommed_KPis = {} #stores recomendation kPIS
    action_KPIs = {}
    RE_chart = {} # recommendation by evaluation
    AS_chart = {} # actions by status
    AE_chart = {} # actions by evaluation


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


    # accepted recommendation count by Evaluation
    tableau_2 = (
    data.loc[data['Recommendation_status'] == "accepté",["N_Recommandation","Evaluation"]]
    .groupby("Evaluation")
    .agg(nb_recomendation=("N_Recommandation","nunique"))
    .reset_index())
    RE_chart = tableau_2.set_index("Evaluation")["nb_recomendation"].to_dict()


    # recommendation by status 
    tableau_3 = (
    data[['Action_id',"Action_status"]]
    .groupby("Action_status")
    .agg(nb_action=("Action_id","nunique"))
    .reset_index()
        )
    RS_chart = tableau_3.set_index("Action_status")["nb_action"].to_dict()


    # Actions count by evaluation
    tableau_4 = (
    data[["Action_id","Evaluation"]]
    .groupby("Evaluation")
    .agg(nb_action=("Action_id","nunique"))
    .reset_index()
    )
    AE_chart = tableau_4.set_index("Evaluation")["nb_action"].to_dict()


    # Taux d’acceptation de recommandation :T1
    T1 = round(results['Nb_accepté'].sum() / results['total_recommendation'].sum(),2) * 100


    # Taux de mise en œuvre des actions : T2
    d = tableau_4.set_index("Action_status")["nb_action"].to_dict()
    T2 = round((d["En continue"] + d["Clôturées"]) / tableau_4.iloc[:,1].sum(), 2) * 100


    # Taux de mise en œuvre des actions critiques : T3
    # ACR : Action Crtitique Realisé
    ACR = data[
        (data["Evaluation"] == "Critique") & 
        (
            (data["Action_status"] == "Clôturées") |
            (data["Action_status"] == "En cours")
        )
        ]['Action_id'].nunique()

    T3 = round(ACR / tableau_4.iloc[:,1].sum(),3) * 100

    action_KPIs=