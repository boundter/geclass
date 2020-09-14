import datetime
import os
import copy
import subprocess
import logging

from flask import current_app
from flask.cli import with_appcontext
import click

from geclass.course_db import CourseDB
from geclass.util.questionnaire_db import QuestionnaireDB
from geclass.util.plots import generate_plots
from geclass.send_email import SendEmail

log = logging.getLogger(__name__)


def sanitize_name(course_name):
    replacements = {
        '\\': '\\textbackslash{}',
        '{': '\{',
        '}': '\}',
        '$': '\$',
        '&': '\&',
        '#': '\#',
        '^': '\\textasciicircum{}',
        '_': '\_',
        '~': '\\textasciitilde{}',
        '%': '\%'
    }
    sanitized_name = ''
    for i in course_name:
        if i in replacements:
            sanitized_name += replacements[i]
        else:
            sanitized_name += i
    return sanitized_name


@click.command('create-reports')
@with_appcontext
def create_reports():
    course_db = CourseDB()
    questionnaire_db = QuestionnaireDB()
    finished_courses = course_db.get_postsurveys_starting_before(
            datetime.timedelta(days=15))
    for (course_id, course_identifier) in finished_courses:
        report_dir = os.path.join(current_app.instance_path, course_identifier)
        if os.path.exists(report_dir):
            continue
        matched_responses = questionnaire_db.get_matched_responses(course_id)
        similar_courses = course_db.get_similar_course_ids(course_id)
        similar_responses = copy.deepcopy(matched_responses)
        for (similar_id,) in similar_courses:
            matched = questionnaire_db.get_matched_responses(similar_id)
            similar_responses.append(matched)
        os.mkdir(report_dir)
        os.chdir(report_dir)
        if matched_responses.size() == 0:
            SendEmail(
                'ge-class@uni-potsdam.de',
                'Kurs {} hat keine gematched Antworten'
                .format(course_identifier),
                'Der Kurs {} mit id {} hat keine gematched Antworten. '
                'Der Report konnte nicht erzeugt werden.'
                .format(course_identifier, course_id)
            )
            log.warning('Course {} with id {}  has no matched responses'
                        .format(course_identifier, course_id))
            continue
        generate_plots(matched_responses, similar_responses)
        count_pre, count_post = questionnaire_db.get_course_numbers(course_id)
        name, count_students = course_db.get_course_report_info(course_id)
        with current_app.open_resource('util/report_template.txt', 'r') as f:
            content = f.read().format(
                course_name=sanitize_name(name),
                course_pre=count_pre,
                course_post=count_post,
                course_matched=matched_responses.size(),
                course_reported=count_students,
                course_ratio=matched_responses.size()/count_students,
                similar_matched=similar_responses.size(),
            )
        with open(os.path.join(report_dir, 'report.tex'), 'w') as f:
            f.write(content)
        latexmk_command = ['latexmk', '-pdf', '-quiet', '-f', 'report.tex']
        latexmk_clean = ['latexmk', '-c', 'report.tex']
        failure = subprocess.call(latexmk_command, stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
        if failure:
            SendEmail(
                'ge-class@uni-potsdam.de',
                'Fehler bei Report für Kurs {}'
                .format(course_identifier),
                'Der Report für den Kurs {} mit id {} konnte nicht '
                'erzeugt werden.'
                .format(course_identifier, course_id)
            )
            log.error('Error while processing of the tex-file for course '
                      '{} with id {}'.format(course_identifier, course_id))
            # TODO: Send email
            continue
        subprocess.call(latexmk_clean, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        click.echo('Generated Report for {} with {} matched responses'
                .format(course_identifier, matched_responses.size()))
    click.echo('Finished Reports')


def init_app(app):
    app.cli.add_command(create_reports)
