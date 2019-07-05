""" Utilities for the enrollments app """
import re

from registrar.apps.core.constants import PROGRAM_KEY_PATTERN
from registrar.apps.core.jobs import processing_job_with_prefix_exists


ENROLLMENT_JOB_NAME_REGEX = re.compile(r'^{}:(.*?)$'.format(PROGRAM_KEY_PATTERN)) 

def build_enrollment_job_status_name(program_key, task_name):
    """
    Build the UserTaskStatus.name for the given task and program

    Arguments:
        program_key (str): program key for the program we're writing enrollments
        task_name (str): the name of the task that is being executed
    """
    return "{}:{}".format(program_key, task_name)

def parse_enrollment_job_status_name(status_name):
    """
    Deconstruct the UserTaskStatus name into program key and task name
    If the name does not match the pattern, return None
    
    Returns:
        (program_key, task_name)
    """
    match = ENROLLMENT_JOB_NAME_REGEX.match(status_name)
    if match:
        return match.groups()

def is_enrollment_job_processing(program_key):
    """
    Returns whether or not a bulk enrollment job for a particular program
    is currently processing (in progress, pending, or retrying)

    Used to ensure only one bulk task can be run at a time for a program.

    Arguments:
        program_key (str): program key for the program we're checking
    """
    program_prefix = build_enrollment_job_status_name(program_key, '')
    return processing_job_with_prefix_exists(program_prefix)
