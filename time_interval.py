"""This module is used to find the interval in seconds for which the update will need to be completed"""

import time

def minutes_to_seconds(minutes):
    """Converts minutes to seconds"""
    return int(minutes)*60

def hours_to_minutes(hours):
    """Converts hours to minutes"""
    return int(hours)*60

def hhmm_to_seconds(hhmm):
    """Converts hours:minutes to seconds"""
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + minutes_to_seconds(hhmm.split(':')[1])

def hhmmss_to_seconds(hhmmss):
    """Converts hours:minutes:seconds to seconds"""
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
          minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])

def interval(update_time):
    """Calulate the interval between the time now and the time at which the update is set to happen"""
    time_now = (str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min) +":" + str(time.gmtime().tm_sec))
    the_interval = hhmm_to_seconds(update_time)-hhmmss_to_seconds(time_now)
    if the_interval < 0:
        the_interval = 86400+the_interval
    return the_interval
    