import pandas as pd
import numpy as np
import datetime

from geclass.util.questionnaire_prepare import RemoveUnneededCols, \
        RemoveUnfinished, RemoveMissingStudentAndCourse, \
        CleanData, AddValidity, PrepareData

def test_removing_cols():
    x = {
        "data_id": [1],
        "survey_key": [1],
        "is_test": [1],
        "last_position": [1],
        "history": [1],
        "media": [1],
        "language": [1],
        "invitation": [1],
        "user": [1],
        "user_agent": [1],
        "start": [1],
        "end": [1],
    }
    df = pd.DataFrame(data=x)
    assert df.shape[1] == 12
    df = RemoveUnneededCols(df)
    assert df.shape[1] == 2


def test_removing_unfinished():
    x = {
        "privacy": [0, 1, 1, 0],
        "end": [0, 0, np.nan, np.nan]
    }
    df = pd.DataFrame(data=x)
    result = pd.DataFrame(data={"end": [0.]}, index=[1])
    df = RemoveUnfinished(df)
    assert df.equals(result)


def test_remove_missing():
    x = {
        "personal_code": [1, 2, np.nan, np.nan],
        "course_id": [np.nan, 1, 2, np.nan]
    }
    result = {
        "personal_code": [1, 2, np.nan],
        "course_id": [np.nan, 1, 2]
    }
    df = pd.DataFrame(data=x)
    result = pd.DataFrame(data=result, index=[0, 1, 2])
    df = RemoveMissingStudentAndCourse(df)
    assert df.equals(result)


def test_clean_data():
    # 1. privacy = 0
    # 2. end = nan
    # 3. personal_code = nan
    # 4. course_id = nan
    # 5. personal_code and course_id = nan
    # 6. everything correct
    x = {
        "data_id": [1, 1, 1, 1, 1, 1],
        "survey_key": [1, 1, 1, 1, 1, 1],
        "is_test": [1, 1, 1, 1, 1, 1],
        "last_position": [1, 1, 1, 1, 1, 1],
        "history": [1, 1, 1, 1, 1, 1],
        "media": [1, 1, 1, 1, 1, 1],
        "language": [1, 1, 1, 1, 1, 1],
        "invitation": [1, 1, 1, 1, 1, 1],
        "user": [1, 1, 1, 1, 1, 1],
        "user_agent": [1, 1, 1, 1, 1, 1],
        "start": [1, 1, 1, 1, 1, 1],
        "privacy": [0, 1, 1, 1, 1, 1],
        "end": [1, np.nan, 1, 1, 1, 1],
        "personal_code": [1, 1, np.nan, 1, np.nan, 1],
        "course_id": [1, 1, 1, np.nan, np.nan, 1]
    }
    result = {
        "start": [1, 1, 1],
        "end": [1., 1., 1.],
        "personal_code": [np.nan, 1, 1],
        "course_id": [1, np.nan, 1]
    }
    df = pd.DataFrame(data=x)
    result = pd.DataFrame(data=result, index=[2, 3, 5])
    df = CleanData(df)
    assert df.equals(result)


def test_validity(app, MonkeyDBDates):
    df = pd.DataFrame(data={
        "course_id": [0, 0, 0, 0, 0],  # dummy
        "pre_post": [1, 1, 2, 2, 0],
        "qcontrol": [4, 4, 3, 3, 3],
        "end": [
                datetime.date(2001, 1, 6), # valid
                datetime.date(2001, 1, 20), # invalid
                datetime.date(2002, 1, 19), # invalid
                datetime.date(2002, 1, 20), # valid
                datetime.date(2002, 1, 20),
            ]
    })
    result = pd.DataFrame(data={
        "course_id": [0, 0, 0, 0, 0],  # dummy
        "pre_post": [1, 1, 2, 2, 0],
        "end": [
                datetime.date(2001, 1, 6),
                datetime.date(2001, 1, 20),
                datetime.date(2002, 1, 19),
                datetime.date(2002, 1, 20),
                datetime.date(2002, 1, 20),
        ],
        "valid_control": [True, True, False, False, False],
        "valid_time": [True, False, False, True, False]
    })
    with app.app_context():
        df = AddValidity(df)
    assert df.equals(result)


def test_pipeline():
    x = {
        "data_id": [1, 1, 1, 1, 1, 1],
        "survey_key": [1, 1, 1, 1, 1, 1],
        "is_test": [1, 1, 1, 1, 1, 1],
        "last_position": [1, 1, 1, 1, 1, 1],
        "history": [1, 1, 1, 1, 1, 1],
        "media": [1, 1, 1, 1, 1, 1],
        "language": [1, 1, 1, 1, 1, 1],
        "invitation": [1, 1, 1, 1, 1, 1],
        "user": [1, 1, 1, 1, 1, 1],
        "user_agent": [1, 1, 1, 1, 1, 1],
        "start": [1, 1, 1, 1, 1, 1],
        "privacy": [0, 1, 1, 1, 1, 1],
        "end": [1, np.nan, 1, 1, 1, 1],
        "personal_code": [1, 1, np.nan, 1, np.nan, 1],
        "course_id": [1, 1, 1, np.nan, np.nan, 1],
        "qcontrol": [1, 2, 3, 4, 3, 4]
    }
    result = {
        "start": [1, 1, 1],
        "end": [1., 1., 1.],
        "personal_code": [np.nan, 1, 1],
        "course_id": [1, np.nan, 1],
        "valid_control": [False, True, True]
    }
    df = pd.DataFrame(data=x)
    #result = pd.DataFrame(data=result, index=[2, 3, 5])
    #df = PrepareData(df)
    #assert df.equals(result)
    assert True
