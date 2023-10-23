from datetime import datetime


def mark_as_invested(db_obj):
    db_obj.fully_invested = True
    db_obj.close_date = datetime.now()
