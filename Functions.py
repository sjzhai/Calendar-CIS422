'''
Adrian Scheuerell, Seth Temple, Shengjie Zhai, Yite Zhao
CIS 422
Simple Calendar Application
4/29/18
'''
from datetime import datetime,date,timedelta
from tkinter import messagebox

def get_weekdays(y,m,d):
    '''(string, string, string) -> list 
        example:
            >>> get_weekday('2018','4','24')
                return['2018-4-23','2018-4-24','2018-4-25','2018-4-26',
                        '2018-4-27','2018-4-28','2018-4-29']
            >>> get_weekday('2018','4','31')
                return False
        By input string of year, month, and day, it will return a list of string of week time.
        If input date incorrect, return False.
    '''
    try:
        yy = int(y)
        mm = int(m)
        dd = int(d)
        day = date(yy,mm,dd)
        t = day.weekday()
        week_start = day + timedelta(days=-t)
        week = [str(week_start + timedelta(i)) for i in range(7)]
        return week
    except:
        return False

def prev_week(w):
    ''' (list) -> list
        Compute string dates for the previous week given week w as a list.
    '''
    monday = w[0]
    if int(monday[:4]) <= 1 and int(monday[5:7]) <= 1 and int(monday[8:]) <= 1: #This breaks the program not caught.
        return w
    monday = date(int(monday[:4]), int(monday[5:7]), int(monday[8:]))
    last_monday = str(monday + timedelta(days=-7))
    return get_weekdays(last_monday[:4], last_monday[5:7], last_monday[8:])

def next_week(w):
    ''' (list) -> list
        Compute string dates for next week given week w as a list.
    '''
    monday = w[0]
    if int(monday[:4]) >= 9999 and int(monday[5:7]) >= 12 and int(monday[8:]) >= 20: #This breaks the program not caught.
        return w
    monday = date(int(monday[:4]), int(monday[5:7]), int(monday[8:]))
    next_monday = str(monday + timedelta(days=7))
    return get_weekdays(next_monday[:4], next_monday[5:7], next_monday[8:])


def get_this_week():
    ''' (None) -> list
        Compute string dates for current week.
    '''
    today = str(datetime.now().date())
    return get_weekdays(today[0:4], today[5:7], today[8:])


def get_labels(start, duration, weekday, weeklist):
    '''(string, string, list, list) -> list
        ("201805011000", 60, [2018-04-30,...,2018-05-06]) -> [self.label[3], self.label[4]]
        Input event start time string, event duration, list of whole week dates, and list of label list.
        Return a list of label in the input date need to add event.
    '''
    label_list = []
    # get information from start time string
    s_day = start[6:8]
    year = start[0:4]
    month = start[4:6]
    s_hour = start[8:10]
    s_min = start[10:12]
    s_label = int(s_hour) * 2
    # due to 30 min for one label, if start time greater than 30, need incremental 1 label.
    if int(s_min) > 30:
        s_label += 1
    left_minute = int(s_hour) * 60 + int(s_min) + int(duration)
    # avoid across the day event
    if left_minute < 1440:
        label = int(duration) // 30
        f_label = s_label + label
        if (int(s_min) + int(duration)) % 30 != 0:
            f_label += 1
        weekday = date(int(year), int(month), int(s_day)).isocalendar()[2]-1
        for i in range(s_label, f_label):
            label_list.append(weeklist[weekday][i])
        return label_list
    


def check_data(event, abb, year, month, day, hour, minutes, duration_hour, duration_minutes,location,detail):
    '''
    check that if data is available for saving to database(such as valid date or valid data followed the requirement)
    return TRUE if data is pass for all requirement raise exception else
    input: strings
    output:True or Exception

    '''
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minutes = int(minutes)
    except:
        return False
        
    if(event == ''):
        messagebox.showinfo('Input', "Please input event name!")
        raise Exception("Please input event name!")
    
    if(abb == ''):
        messagebox.showinfo('Input', "please input abbreviation!")
        raise Exception("please input abbreviation!")
    elif len(abb) > 10:
        messagebox.showinfo('Input Limit', "Please keep the abbreviation under 10 characters.")
        raise Exception("Please keep the abbreviation under 10 characters.")

    if(year == ''):
        messagebox.showinfo('Input', "Please input year!")
        raise Exception("Please input year!")

    if(month == ''):
        messagebox.showinfo('Input', "Please input month!")
        raise Exception("Please input month!")

    if(day == ''):
        messagebox.showinfo('Input', "Please input day!")
        raise Exception("Please input day!")

    if(hour == ''):
        messagebox.showinfo('Input', "Please input hour!")
        raise Exception("Please input hour!")

    if(minutes == ''):
        messagebox.showinfo('Input', "Please input minutes!")
        raise Exception("Please input minutes!")

    if(duration_hour == ''):
        messagebox.showinfo('Input', "Please select duration hours!")
        raise Exception("Please select duration hours!")

    if(duration_minutes == ''):
        messagebox.showinfo('Input', "Please select duration minutes!")
        raise Exception("Please select duration minutes!")

    if duration_hour == str(0) and duration_minutes == str(0):
        messagebox.showinfo('Input', "Events must be noninstantaneous.")
        raise Exception("Events must be noninstantaneous.")
    
    try:
        years = int(year)
        months = int(month)
        days = int(day)
        hours = int(hour)
        minutes_ = int(minutes)
    except:
        messagebox.showinfo('Input Limit', "date or time should be integer.")
        raise Exception("date or time should be integer.")

    try:
        day = date(years,months,days)

    except: 
        messagebox.showinfo('Input Limit', "Sorry! the input date is not rational.")
        raise Exception("Sorry! the input date is not rational.")

    if int(hours > 23 or hours < 0 or minutes_ > 59 or minutes_ < 0):
        messagebox.showinfo('Input Limit', "Sorry! hour should be <= 23 and >= 0, minutes should be <= 59 and >= 0.")
        raise Exception("Sorry! hour should be <= 23 and >= 0, minutes should be <= 59 and >= 0.")


    if int(hour) + int(duration_hour) > 24:
        left_hour = 24 - int(hour)
        messagebox.showinfo('Across Day Event', "Event duration time would no greater than "+ str(left_hour) +" hour(s).")
        raise Exception("Event duration time would no greater than "+ str(left_hour) +" hour(s).")
    elif int(hour) + int(duration_hour) == 24:
        if int(minutes) + int(duration_minutes) > 0:
            messagebox.showinfo('Across Day Event', "Cannot add more minutes for event duration.")
            raise Exception("Cannot add more minutes for event duration.")  

    if len(location)>9999 or len(abb)>9999 or len(event)>9999 or len(detail)>9999:
        messagebox.showinfo('Input Limit', "Please limit inputs in all fields to under 10,000 characters.")
        raise Exception("Please limit inputs in all fields to under 10,000 characters.")
    

    '''
    if year >= 9999 or month >= 12 or day > 26:
        messagebox.showinfo('Input Limit', "Sorry! Dates beyond 9999-12-26 are not allowed.")
        raise Exception("Sorry! Dates beyond 9999-12-26 are not allowed.")
    elif year <= 0 or month <= 0 or day <= 0:
        messagebox.showinfo('Input Limit', "Sorry! 0001-01-01 is the earliest allowed date.")
        raise Exception("Sorry! 0001-01-01 is the earliest allowed date.")
    '''
    return True


def check_input_date(year, month, day):
    '''(string, string, string) -> Boolean
        This ensures data entered into the input date field can be checked without causing errors.
    '''
    try:
        y = int(year)
        m = int(month)
        d = int(day)
        if y == 9999 and m == 12 and d > 26: #Both of these cases completely break the program.
            messagebox.showinfo('Warning', "Sorry! Dates beyond 9999-12-26 are not allowed.")
            raise Exception("Sorry! Dates beyond 9999-12-26 are not allowed.")
        elif y <= 0:
            messagebox.showinfo('Warning', "Sorry! 0001-01-01 is the earliest allowed date.")
            raise Exception("Sorry! 0001-01-01 is the earliest allowed date.")
        return True
    except ValueError:
        return False

    
