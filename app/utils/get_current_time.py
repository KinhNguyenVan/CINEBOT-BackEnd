from datetime import datetime
from zoneinfo import ZoneInfo  

def get_current_time_by_timezone():
    now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    return now.strftime("%A, %d/%m/%Y %H:%M")