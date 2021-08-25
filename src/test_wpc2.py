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

    current_date = datetime.datetime(2021, 8, 13, hour=6, minute=36, second=10) 
    next_date = get_next_timeslot_date(current_date, 20)
    assert(next_date.minute == 36)
    assert(next_date.second == 20)
    assert(next_date.microsecond == 0)
        
def test_get_post_id():
    target_blog = "http://127.0.0.3/"
    exfil_channel = "2021/08/13/exfil-channel/"
    ack_channel = "2021/08/13/ack-channel/"

    assert(get_post_id(target_blog, exfil_channel) == 5)
    assert(get_post_id(target_blog, ack_channel) == 7)

def test_generate_random_spam_comment():
    comment = generate_random_spam_comment(0)
    assert(comment == "Mannabase is a new Cryptocurrency is actually giving away FREE coins every week to new users. The best part is they are a Humanitaraian organization set to be bigger than Bitcoin. This could be the Biggest investment you ever make. If you have 5 Minutes to spare read the Whitepaper these Guys are something else. https://www.mannabase.co/join/")
    
    
