import sqlCalendarLogic
import CalendarEvent
import os

def db_create():
    try:
        os.remove("testdb1")
    except:
        pass
    testdb1 = sqlCalendarLogic.connect_to_db("testdb1")
    assert os.path.isfile("testdb1")
    print("Test database created successfully")
    return testdb1

def calendar_create(testdb1):
    assert not sqlCalendarLogic.check_for_table(testdb1,"test1")
    sqlCalendarLogic.make_calendar(testdb1, "test1")
    assert sqlCalendarLogic.check_for_table(testdb1,"test1")
    assert not sqlCalendarLogic.check_for_table(testdb1,"test2")
    assert sqlCalendarLogic.get_tables(testdb1) == ["test1","sqlite_sequence"]
    sqlCalendarLogic.make_calendar(testdb1, "test2")
    try:
        sqlCalendarLogic.make_calendar(testdb1, "")
    except:
        pass
    long_string = ""
    for i in range(300):
        long_string+=(str(i))
    try:
        sqlCalendarLogic.make_calendar(testdb1, long_string)
    except:
        pass
    #need to, at some point in the process, catch these so they don't crash the program
    assert sqlCalendarLogic.get_tables(testdb1) == ["test1","sqlite_sequence","test2"]
    print("Test calendar created successfully")

def event_create(testdb1):
    event1 = CalendarEvent.CalendarEvent("event1","e1",1,1,2018,4,19,1,"d1","p1","c1")
    sqlCalendarLogic.add_event(testdb1,"test1",event1)
    fetched = sqlCalendarLogic.get_new_week(testdb1,"test1",2018,4,19)
    assert len(fetched) == 1
    fetched = sqlCalendarLogic.get_new_week(testdb1,"test1",2015,4,19)
    assert len(fetched) == 0
    event2 = CalendarEvent.CalendarEvent("","",1,1,2018,4,18,0,"","","") #I am not sure if we want this to be valid or not.
    sqlCalendarLogic.add_event(testdb1,"test1",event2)
    fetched = sqlCalendarLogic.get_new_week(testdb1,"test1",2018,4,19)
    assert len(fetched) == 2
    #event3 = CalendarEvent.CalendarEvent("","",0,0,0,0,0,0,"","","") This one is invalid, but again, I'm not sure where these should be caught. Will mention in meeting
    #sqlCalendarLogic.add_event(testdb1,"test1",event3)
    #Will write more after discussing this and how IDs should be fetched.

if __name__ == "__main__":
    testdb1 = db_create()
    calendar_create(testdb1)
    event_create(testdb1)
    
    
