import pandas as pd
import datetime

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


def CleanData(df):
    rows_before = df.shape[0]
    df = (df
        .pipe(RemoveUnneededCols)
        .pipe(RemoveUnfinished)
        .pipe(RemoveMissingStudentAndCourse)
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
    df["valid_control"] = df.apply(
            lambda row: CheckValidityControlRow(row), axis=1)
    df = df.drop(["qcontrol"], axis=1)
    course_db = CourseDB()
    df["valid_time"] = df.apply(
            lambda row: CheckValidityTimeRow(row, course_db), axis=1)
    return df


def PrepareData(df):
    df = (df
        .pipe(CleanData)
        .pipe(ChangeStartAndEndToDatetime)
        .pipe(AddValidity)
    )
    return df
