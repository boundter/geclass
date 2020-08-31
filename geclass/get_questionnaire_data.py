import pandas as pd

from geclass.questionnaire_prepare import PrepareData
from geclass.questionnaire_db import QuestionnaireDB

def LoadQuestionnaireData(file_location):
    data = pd.read_excel("data.xlsx")
    df = PrepareData(data)
    questionnaire_db = QuestionnaireDB()
    questionnaire_db.insert_data(df)
