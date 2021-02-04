import click
from flask.cli import with_appcontext
import pandas as pd

from geclass.course_db import CourseDB
from geclass.util.questionnaire_db import QuestionnaireDB


@click.command('export_to_csv')
@with_appcontext
def export():
    """Export all matched responses to a csv at /app/instace/export.csv."""
    cols = ["course_id",
            "experience_id",
            "program_id",
            "course_type_id",
            "traditional_id",
            *["q_you_pre_" + str(i) for i in range(1, 31)],
            *["q_you_post_" + str(i) for i in range(1, 31)],
            *["q_expert_pre_" + str(i) for i in range(1, 31)],
            *["q_expert_post_" + str(i) for i in range(1, 31)],
            *["q_mark_" + str(i) for i in range(1, 23)],
    ]
    data = {}
    for col in cols:
        data[col] = []
    course_db = CourseDB()
    questionnaire_db = QuestionnaireDB()
    course_data = list(course_db.get_all_course_data())
    for course in course_data:
        course_id = course["id"]
        metadata_name = (
                "experience_id", "program_id", "course_type_id",
                "traditional_id")
        metadata = [course[name] for name in metadata_name]
        matched = questionnaire_db.get_matched_responses(course_id)
        for i in range(matched.size()):
            data["course_id"].append(course_id)
            for indx, col in enumerate(metadata_name):
                data[col].append(metadata[indx])
            for indx in range(1, 31):
                data["q_you_pre_" + str(indx)].append(
                    matched.q_you_pre.responses[i][indx-1]
                )
                data["q_you_post_" + str(indx)].append(
                    matched.q_you_post.responses[i][indx-1]
                )
                data["q_expert_pre_" + str(indx)].append(
                    matched.q_expert_pre.responses[i][indx-1]
                )
                data["q_expert_post_" + str(indx)].append(
                    matched.q_expert_post.responses[i][indx-1]
                )
            for indx in range(1, 23):
                data["q_mark_" + str(indx)].append(
                    matched.q_mark.responses[i][indx-1]
                )
    df = pd.DataFrame(data)
    # shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv("/app/instance/export.csv")


def init_app(app):
    app.cli.add_command(export)
