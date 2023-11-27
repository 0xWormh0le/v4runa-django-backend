import datetime

def get_choice_id_by_label(label, choices):
    for item in choices:
        if item[1] == label:
            return item[0]
    return None


def get_current_year():
    return datetime.date.today().year


def get_next_job_number(job_number = None):
    if not job_number:
        return datetime.date.today().year * 100000 + 1
    return int(job_number) + 1
