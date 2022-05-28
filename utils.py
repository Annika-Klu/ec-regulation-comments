from datetime import datetime

def current_date_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")