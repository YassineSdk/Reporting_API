from services.validation import Validate_data
import pandas as pd 




def test_validation_data():
    data = pd.read_csv("/home/yassine/ONCF_projects/Reporting_API/mock_data.csv")
    results = Validate_data(data) 
    assert isinstance(results,pd.DataFrame)

