import sys
sys.path.append("../src")
import datetime
from wpc2 import *

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
    AUTH_KEY = "0c008b2f27fbaf5e9acaaa08bf251fc98c6d38a1"
    AUTH_SALT = "ea30c9849bfd208c9890cbf7bb56f59a20b52c4f"
    
    posted_date = "2021-08-09 06:11:11"
    computed_hash = compute_moderation_hash(posted_date, AUTH_KEY, AUTH_SALT)
    assert("0d36c71955cc6fc19fb31501132cfdb1" == computed_hash)

def test_timeslot():
    current_date = datetime.datetime(2021, 8, 11, minute=23, second=0) 
    next_date = get_next_timeslot_date(current_date, 44)
    assert(next_date.minute == 23)
    assert(next_date.second == 44)
    assert(next_date.microsecond == 0)

    next_date = get_next_timeslot_date(current_date, 11)
    assert(next_date.minute == 23)
    assert(next_date.second == 11)
    assert(next_date.microsecond == 0)

    current_date = datetime.datetime(2021, 8, 13, hour=1, minute=41, second=38) 
    next_date = get_next_timeslot_date(current_date, 11)
    assert(next_date.minute == 42)
    assert(next_date.second == 11)
    assert(next_date.microsecond == 0)
        
def test_get_post_id():
    target_blog = "http://127.0.0.3/"
    exfil_channel = "2021/08/13/exfil-channel/"
    ack_channel = "2021/08/13/ack-channel/"

    assert(get_post_id(target_blog, exfil_channel) == 5)
    assert(get_post_id(target_blog, ack_channel) == 7)
