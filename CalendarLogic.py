'''
Adrian Scheuerell, Seth Temple, Shengjie Zhai, Yite Zhao
CIS 422
Simple Calendar Application
4/29/18
'''

import sqlite3
from datetime import date
from datetime import datetime
from CalendarEvent import *
from tkinter import messagebox
import builtins

builtins.unsaved = True
def load_calendar_model(db):
    '''(str) -> sqlite3.Connection
    Either connects to a database or creates a database with one table calendar_model.
    Compatible as a GUI tkinter Button command.
    db is a string name for a .db file.
    Returns a sqlite3.Connection to a database with one table calendar_model.
    '''

    def connect_to_db(db):
        '''(str) -> sqlite3.Connection
        Either sets up a sqlite3 connection to a .db file, or makes a new .db file.
        '''
        return sqlite3.connect(db)

    def check_for_table(db):
        '''(sqlite3.Connection) -> bool
        Fetches a list of all the table names in a database, and evaluates if there is a calendar table
        in the database.
        Returns True or False.
        '''
        c = db.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' ;")
        fetch = c.fetchall()
        return (len(fetch) != 0)

    def make_calendar(db):
        '''(sqlite3.Connection) -> None
        Makes a table in the .db. The table represents an empty calendar.
        '''
        db.cursor().execute("CREATE TABLE calendar_model (Event STRING, Abbreviation STRING,\
                            Start SMALLDATETIME, End SMALLDATETIME,\
                            Hour INTEGER, Minute INTEGER,\
                            Year INTEGER, Month INTEGER, Day INTEGER, Week INTEGER, Weekday INTEGER,\
                            Duration INTEGER, Detail STRING, Place STRING, Category STRING) ;")
        db.commit()

    database = connect_to_db(db)
    if not(check_for_table(database)):
        make_calendar(database)
    return database

def raise_timeconflict(db, event, datetime=None):
    ''' (sqlite3.Connection, CalendarEvent) -> None
    Raises an error when the event has a time conflict with an event already in the database.
    '''
    # special case handling time conflicts while updating
    if datetime != None:
        c = db.cursor().execute("SELECT Start, End FROM calendar_model WHERE Start != :d and :s BETWEEN Start and End ;",
                         {'d':datetime, 's':event.timedate()})
        C = db.cursor().execute("SELECT Start, End FROM calendar_model WHERE Start != :d and :e BETWEEN Start and End ;",
                           {'d':datetime, 'e':event.end_datetime()})
        
    # general case that handles time conflicts while adding   
    else:
        c = db.cursor().execute("SELECT Start, End FROM calendar_model WHERE :s BETWEEN Start and End ;",
                         {'s':event.timedate()})
        C = db.cursor().execute("SELECT Start, End FROM calendar_model WHERE :e BETWEEN Start and End ;",
                           {'e':event.end_datetime()})
        
    if (len(C.fetchall()) + len(c.fetchall())) > 0:
        messagebox.showinfo('Time Conflict', 'Time conflict with another event.')
        raise ValueError('Time conflict with another event.')

def add_event(db, event):
    '''(sqlite3.Connection, CalendarEvent) -> None
    Includes a row in a SQL table. The table represents a calendar and the row represents an event.
    '''
    raise_timeconflict(db, event)
    db.cursor().execute("INSERT INTO calendar_model (Event, Abbreviation, Start, End,\
                        Hour, Minute,\
                        Year, Month, Day, Week, Weekday,\
                        Duration, Detail, Place, Category) \
                        VALUES (:name, :abbrev, :start, :end,\
                        :hr, :mt, :yr, :mn, :dy, :wk, :wkd,\
                        :dur, :detail, :loc, :cat) ;", {'name':event.event(),
                                                       'abbrev':event.abbreviation(),
                                                       'start':event.timedate(),
                                                       'end':event.end_datetime(),
                                                       'hr':event.hour(),
                                                       'mt':event.minute(),
                                                       'yr':event.year(),
                                                       'mn':event.month(),
                                                       'dy':event.day(),
                                                       'wk':event.week(),
                                                       'wkd':event.weekday(),
                                                       'dur':event.duration(),
                                                       'detail':event.detail(),
                                                       'loc':event.place(),
                                                       'cat':event.category()})
    builtins.unsaved = False
    

# add_event(sqlite3.connect('sss.db'), CalendarEvent('jcnak', 'cnkas', '5', '14', '2018', '4', '25', '90', 'detail', 'place', 'yellow'))
def add_recurring_events(db, event, freq, length):
    '''
    
    '''
    if freq == 'Weekly':
        days = 7
    elif freq == 'Biweekly':
        days = 14
    elif freq == 'Monthly':
        days = 28
    
    length = int(length)
    pass
    
def save_changes(db):
    db.commit()
    builtins.unsaved = True
    
def update_event(db, event, dt):
    '''(sqlite3.Connection, CalendarEvent, str) -> None
    Edit in the SQL table the row corresponding to Start datetime with a new CalendarEvent event.
    '''
    raise_timeconflict(db, event, dt)
    db.cursor().execute("UPDATE calendar_model SET Event = :name, Abbreviation = :abbrev, Start = :start, End = :end,\
                        Hour = :hr, Minute = :mt,\
                        Year = :yr, Month = :mn, Day = :dy, Week = :wk, Weekday = :wkd,\
                        Duration = :dur, Detail = :detail, Place = :loc, Category = :cat WHERE Start = :datetime ;",
                        {'name':event.event(),
                         'abbrev':event.abbreviation(),
                         'start':event.timedate(),
                         'end':event.end_datetime(),
                         'hr':event.hour(),
                         'mt':event.minute(),
                         'yr':event.year(),
                         'mn':event.month(),
                         'dy':event.day(),
                         'wk':event.week(),
                         'wkd':event.weekday(),
                         'dur':event.duration(),
                         'detail':event.detail(),
                         'loc':event.place(),
                         'cat':event.category(),
                         'datetime':dt})
    builtins.unsaved = False

def delete_event(db, dt):
    '''(sqlite3.Connection, str) -> None
    Removes an event from a SQL table that contains the unique Start datetime.
    '''
    db.cursor().execute("DELETE FROM calendar_model WHERE Start = :datetime ;", {'datetime':dt})
    builtins.unsaved = False
    
def get_new_week(db, year, month, day):
    '''(sqlite3.Connection, str/int, str/int, str/int) -> list
    Given a date, this function returns a list of CalendarEvent objects in a SQL table that occur in that week.
    '''
    yr = int(year)
    wk = date(yr, int(month), int(day)).isocalendar()[1]
    data = db.cursor().execute("SELECT * FROM calendar_model WHERE Week = :wk AND Year = :yr ;",
                               {'wk':wk, 'yr':yr})
    calendar_events = [CalendarEvent(item[0], item[1], item[4], item[5], 
                                    item[6], item[7], item[8],
                                    item[11], item[12], item[13], item[14]) for item in data.fetchall()]
    return calendar_events

def get_db_name(db):
    ''' (sqlite3.Connection) -> str
    Gets the name of the connected database via string processing.
    Returns the database name.
    '''
    c = db.cursor().execute("PRAGMA database_list ;")
    path = c.fetchall()[0][2]
    
    boolean = True
    while boolean:
        i = path.find('\\') # find the first \\
        if i == -1:
            boolean = False # condition to stop while loop
        else:
            path = path[i+1:] # slice based on index of first \\
    return path[:-3] # remove .db

def load_db_name(directory):
    ''' (str) -> str
        input the local directory of the database file and return the name of .db file.
    '''
    db_dir = directory
    boolean = True
    while boolean:
        i = db_dir.find("/")
        if i == -1:
            boolean = False
        else:
            db_dir = db_dir[i+1:]
    return db_dir




def backup_calendar(db):
    '''(sqlite3.Connection) -> None
    Backs up .db info to a comma separated values file.
    Calls get_db_name.
    Returns None.
    '''
    columns = db.cursor().execute("PRAGMA table_info(calendar_model) ;").fetchall() # query table columns
    query = db.cursor().execute("SELECT * FROM calendar_model ORDER BY Start ;") # query rows sorted by datetime
    
    dt = str(datetime.now())[:10] # name backup file by datetime created
    with open(get_db_name(db) + '-backup-' + dt + '.csv', 'w') as f:
        
        # write column names to file
        for c in columns:
            f.write(c[1] + '\t')
        f.write('\n')
        
        # write row data to file
        for row in query:
            for col in row:
                f.write(str(col) + '\t')
            f.write('\n')