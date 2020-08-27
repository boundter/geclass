import pandas as pd

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


def AddValidity(df):
    df["valid_control"] = df.apply(
            lambda row: CheckValidityControlRow(row), axis=1)
    df = df.drop(["qcontrol"], axis=1)
    #TODO: Check end time
    return df


def PrepareData(df):
    df = (df
        .pipe(CleanData)
        .pipe(AddValidity)
    )
    return df
