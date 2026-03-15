from datetime import date

def check_deadline_status(deadline):

    today = date.today()
    days_left = (deadline - today).days

    if days_left < 0:
        return "OVERDUE"

    elif days_left <= 3:
        return "DUE_SOON"

    else:
        return "SAFE"