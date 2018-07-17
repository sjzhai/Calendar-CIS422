'''
Adrian Scheuerell, Seth Temple, Shengjie Zhai, Yite Zhao
CIS 422
Simple Calendar Application
4/24/18
'''

from datetime import time, date, timedelta
from datetime import datetime as dt

class CalendarEvent:
    '''
    Custom class to encapsulate calendar event data.
    An event has a name, an abbreviation, a time, a date, a duration, a description,
    a location, and a category.
    Getter methods available.
    '''
    def __init__(self, event, abbreviation, hour, minutes, year, month, day, duration, detail, place, category):
        self._event = event
        self._abbreviation = abbreviation
        self._datetime = dt(int(year), int(month), int(day), int(hour), int(minutes))
        self._duration = int(duration)
        self._detail = detail
        self._place = place
        self._category = category
    
    # getter methods
    def event(self):
        return self._event
    def abbreviation(self):
        return self._abbreviation
    def timedate(self):
        return str(self._datetime)
    def hour(self):
        return self._datetime.hour
    def minute(self):
        return self._datetime.minute
    def day(self):
        return self._datetime.day
    def month(self):
        return self._datetime.month
    def year(self):
        return self._datetime.year
    def duration(self):
        return self._duration
    def detail(self):
        return self._detail
    def place(self):
        return self._place
    def category(self):
        return self._category
    
    def end_datetime(self):
        '''Compute finish datetime based on the start datetime and duration of the event.'''
        hrs = self._duration // 60
        mins = self._duration % 60
        delta = self._datetime + timedelta(hours=hrs, minutes=mins, seconds=-1)
        return str(delta)
        
    def week(self):
        '''Returns the week of the year. App uses this method to switch weeks on the calendar.'''
        return self._datetime.isocalendar()[1]
    def weekday(self):
        '''Returns the weekday given a date. App uses this method to match dates with SMTWRFS.'''
        return self._datetime.isocalendar()[2]