import datetime
from server import *

def test_get_previous_valid_timeslot_date():
    current_date = datetime.datetime(2021, 1, 2, hour=13, minute=26, second=26)
    time_slot = "1:11"
    timeslot_date = get_previous_valid_timeslot_date(current_date, time_slot)
    assert(timeslot_date.minute == 21)
    assert(timeslot_date.second == 11)
