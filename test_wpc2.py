import datetime
from server import *

def test_get_previous_valid_timeslot_date():
    time_slot = "1:11"

    current_date = datetime.datetime(2021, 1, 2, hour=13, minute=26, second=26)
    timeslot_date = get_previous_valid_timeslot_date(current_date, time_slot)
    assert(timeslot_date.minute == 21)
    assert(timeslot_date.second == 11)

    current_date = datetime.datetime(2021, 1, 2, hour=13, minute=20, second=26)
    timeslot_date = get_previous_valid_timeslot_date(current_date, time_slot)
    assert(timeslot_date.minute == 11)
    assert(timeslot_date.second == 11)

    current_date = datetime.datetime(2021, 1, 2, hour=13, minute=2, second=26)
    timeslot_date = get_previous_valid_timeslot_date(current_date, time_slot)
    assert(timeslot_date.minute == 1)
    assert(timeslot_date.second == 11)

    current_date = datetime.datetime(2021, 1, 2, hour=13, minute=0, second=26)
    timeslot_date = get_previous_valid_timeslot_date(current_date, time_slot)
    assert(timeslot_date.minute == 51)
    assert(timeslot_date.second == 11)

def test_compute_moderation_hash():
    posted_date = "2021-08-09 06:11:11"
    computed_hash = compute_moderation_hash(posted_date)
    assert("0d36c71955cc6fc19fb31501132cfdb1" == computed_hash)
