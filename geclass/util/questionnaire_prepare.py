"""Functions to clean the data from the questionnaire.

The function PrepareData fully cleans the data and checks for validity.

"""

import datetime

import pandas as pd

from geclass.course_db import CourseDB

def RemoveUnneededCols(df):
    to_remove = [
        "data_id",
        "survey_key",
        "is_test",
        "last_position",
        "history",
        "media",
        "language",
        "invitation",
        "user",
        "user_agent",
    ]
    df = df.drop(to_remove, axis=1)
    return df


def RemoveUnfinished(df):
    df = df[df.privacy == 1]
    df = df.drop(["privacy"], axis=1)
    df = df.dropna(subset=["end"])
    return df


def RemoveMissingStudentAndCourse(df):
    return df[~(df.personal_code.isna()) | ~(df.course_id.isna())]


def ChangeStartAndEndToDatetime(df):
    df.start = pd.to_datetime(df.start)
    df.end = pd.to_datetime(df.end)
    return df


def LowercaseCodes(df):
    df.personal_code = df.personal_code.str.lower()
    df.course_id = df.course_id.str.lower()
    return df


def CleanData(df):
    """Clean the data.

    1. Remove unnecessary columns.
    2. Remove unfinished rows (no end date or no privacy agreement).
    3. Remove rows with missing student or course information.
    4. Change personal codes and course id to lowercase for consitency.
    5. Change start and entime cols to datetime.

    """
    df = (df
        .pipe(RemoveUnneededCols)
        .pipe(RemoveUnfinished)
        .pipe(RemoveMissingStudentAndCourse)
        .pipe(LowercaseCodes)
        .pipe(ChangeStartAndEndToDatetime)
    )
    return df


def CheckValidityControlRow(row):
    # control question needs to be answered "stimme eher zu" = 4
    return row.qcontrol == 4


def CheckValidityTimeRow(row, course_db):
    course_times = course_db.get_course_questionnaire_dates(row["course_id"])
    if row["pre_post"] == 1 and course_times is not None:
        min_time = datetime.date.fromtimestamp(int(course_times["pre"]))
        max_time = min_time + datetime.timedelta(days=14)
        return row["end"] >= min_time and row["end"] <= max_time
    elif row["pre_post"] == 2 and course_times is not None:
        min_time = datetime.date.fromtimestamp(int(course_times["post"]))
        max_time = min_time + datetime.timedelta(days=14)
        return row["end"] >= min_time and row["end"] <= max_time
    return False


def AddValidity(df):
    """Check validity of row.

    valid_control tests for the correct answer of the control question and
    valid_time tests for if the end date is within 14 days of the begin of the
    post test.

    """
    df["valid_control"] = df.apply(
            lambda row: CheckValidityControlRow(row), axis=1)
    df = df.drop(["qcontrol"], axis=1)
    course_db = CourseDB()
    df["valid_time"] = df.apply(
            lambda row: CheckValidityTimeRow(row, course_db), axis=1)
    return df


def PrepareData(df):
    """Fully clean the data."""
    df = (df
        .pipe(CleanData)
        .pipe(AddValidity)
    )
    return df
