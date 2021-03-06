'''
Adrian Scheuerell, Seth Temple, Shengjie Zhai, Yite Zhao
CIS 422
Simple Calendar Application
4/23/18
'''
#It would probably be a good idea to comment out the line of code at the bottom in the exception handler that prints the error details before submitting the assignment. It's pretty much necessary for debugging though.

# Reference some required python module syntax
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from time import *
import datetime
# Reference SQL database file, assist SQL file, and assist functions file
import CalendarLogic as CL
import CalendarEvent as CE
import functions as AF
# A function tool assist labels bind pop-up windows
from functools import partial
# Get boolean value assist whether close window
import builtins
import traceback


class Calendar(Frame):

    def __init__(self, master, _year=None, _month=None, _day=None, _week=[], _database=None, _fulldatetime=None):
        Frame.__init__(self, master)

        self.year = _year
        self.month = _month
        self.day = _day
        self.week = _week
        self.database = _database
        self.fulldatetime = _fulldatetime

        # init 8 lists to store calendar labels, it is easy to get location
        self.Daylist = []
        self.Sunlist = []
        self.Monlist = []
        self.Tuelist = []
        self.Wedlist = []
        self.Thulist = []
        self.Frilist = []
        self.Satlist = []
        self.day_list = [self.Sunlist, self.Monlist, self.Tuelist, self.Wedlist, self.Thulist, self.Frilist, self.Satlist]

        self.widget_button_labelframe()
        self.mainframe = LabelFrame(master)
        self.mainframe.grid(row=0, column=1, padx=0, pady=15, sticky=N+W)
        self.widget_date_labelframe(self.mainframe)
        self.info_labelframe(self.mainframe)
        self.widget_label_labelframe(self.mainframe)
        self.widget_event_labelframe(self.mainframe)


    def set_year(self, year):
        self.year = year
    def set_month(self, month):
        self.month = month
    def set_day(self, day):
        self.day = day
    def set_week(self, week):
        self.week = week
    def set_database(self, db):
        self.database = db
    def set_fulldatetime(self, fdatetime):
        self.fulldatetime = fdatetime
    def get_year(self):
        return self.year
    def get_month(self):
        return self.month
    def get_day(self):
        return self.day
    def get_week(self):
        return self.week
    def get_database(self):
        return self.database
    def get_fulldatetime(self):
        return self.fulldatetime

    def widget_button_labelframe(self):
        '''(None) -> None
            Create a button labelframe on left side,
            it include 'ADD', 'SAVE', 'NEW', and 'LOAD' buttons.
        '''
        def newWin():
            '''(None) -> None
               This function is command function for ADD button,
               click ADD button to pop-up new window.
            '''
            if self.namelabel['text'] == 'NAME':
                messagebox.showinfo(title='Add Event Alert', message="You cannot add a event without name. Please load a '.db' file by click 'LOAD' button or create a new name by click 'NEW' button.")
            else:
                self.AddInfo()

        def save_db():
            CL.save_changes(self.get_database())
            # print(CL.get_db_name(self.get_database()))
            # c = (self.get_database().cursor().execute("SELECT * FROM calendar_model;"))
            # print(c.fetchall())
            # self.get_database().commit()

        def nameDB():
            '''(None) -> None
               This function is command function for 'NEW' button,
               click NEW button to pop-up new window.
               'CONFIRM' button can store name
            '''
            def namebutton_clicked():
                '''(None) -> None
                    Command function for 'CONFIRM' button,
                    Pop-up ask Yes or No message box can make user double check.
                    If user click 'yes', it can change the 'NAME' above the calendar
                '''
                self.quit = False
                y_or_n = messagebox.askyesno('Verify', 'Are you sure the name for new DB?')
                if y_or_n:
                    self.namelabel['text'] = self.nametext.get()
                    db_name = self.nametext.get()+'.db'
                    db = CL.load_calendar_model(db_name)
                    self.set_database(db)
                    self.name.destroy()

            if self.namelabel['text'] != 'NAME':
                messagebox.showinfo(title='NEW button Waring message', message="You already chose a name for your database.")
            else:
                self.name = Toplevel()
                self.name.resizable(width=False, height=False)
                self.name_label = Label(self.name, text='Input a name for a new database:').grid(row=0, column=0, sticky=W)
                self.nametext = StringVar()
                self.name_entry = Entry(self.name, width=25, textvariable=self.nametext).grid(row=1, column=0, sticky=W)
                self.name_button = Button(self.name, text='CONFIRM', width=7, height=1, command=namebutton_clicked).grid(row=2, column=0)
                

        '''NEED TO IMPLEMENT MORE '''
        def openfiles():
            '''(None) -> None
               open ".db" files from local directories
            '''
            filename= askopenfilename(filetypes=(("SQL", ".db"),("All files", "*.*")))
            if filename:
                db_name = CL.load_db_name(filename)
                name = db_name[:-3]
                messagebox.showinfo(title='Load File Message', message="Sucessfully Load database File: \n'%s'" % name)
                db = CL.load_calendar_model(db_name)
                self.set_database(db)
                self.namelabel['text'] = name

                week = AF.get_this_week()
                y = week[0][0:4]
                m = week[0][5:7]
                d = week[0][8:10]
                events = CL.get_new_week(db, y, m, d)
                
                for event in events:
                    timedate = event.timedate()
                    Time = timedate[0:10]
                    if Time in AF.get_this_week():
                        duration = event.duration()
                        s_time = timedate[0:4]+timedate[5:7]+timedate[8:10]+timedate[11:13]+timedate[14:16]+timedate[17:]
                        labels = AF.get_labels(s_time, duration, week, self.day_list)
                        for label in labels:
                            label['text'] = event.abbreviation()
                            label['bg'] = event.category()

        self.buttonframe = LabelFrame(self.master)
        self.buttonframe.grid(row=0, column=0, padx=15, pady=15, sticky=N+W)
        self.titleLabel = Label(self.buttonframe, text='OPTIONS', borderwidth=2, relief='groove', width=8, height=1)
        self.titleLabel.grid(row=0, column=0, pady=3)
        # create "ADD" button to add event
        self.addButton = Button(self.buttonframe, text='ADD', width=6, height=1, command=newWin)
        self.addButton.grid(row=1, column=0, pady=3)
        # create "SAVE" button to save information input at the bottom
        self.saveButton = Button(self.buttonframe, text='SAVE', width=6, height=1, command=save_db)
        self.saveButton.grid(row=2, column=0, pady=3)
        # create "NEW" button to allow user input new database name
        self.newButton = Button(self.buttonframe, text='NEW', width=6, height=1, command=nameDB)
        self.newButton.grid(row=3, column=0, pady=3)
        # create "LOAD" button to retrive and show event on calendar
        self.loadButton = Button(self.buttonframe, text='LOAD', width=6, height=1, command=openfiles)
        self.loadButton.grid(row=4, column=0, pady=3)
       

    def widget_date_labelframe(self, mainframe):
        '''(mainframe) -> None
            This date labelframe build on mainframe,
            user can input information in entries.
            'Enter' button can arrange data and show dates by change date above "Mon, Tue,...".
        '''

        def getDate():
            '''(None) -> None
                This function is command function for 'ENTER' button.
                It has
            '''
            y = self.ytext.get().strip(' ')
            m = self.mtext.get().strip(' ')
            d = self.dtext.get().strip(' ')

            def isLeap(year):
                '''(year) -> bool
                   Simply input year and function determines that the year
                   is leap year or not, then return True or False.
                '''
                if (year % 4) == 0:
                    if (year % 100) == 0:
                        if (year % 400) == 0:
                            return True
                        else:
                            return False
                    else:
                        return True
                else:
                    return False
                
            if AF.check_input_date(y,m,d): #This will run some extra checks to make sure the checks below can run without causing errors.
                if len(y) == 4 and len(m) <= 2 and len(d) <= 2: # determine input range
                    if int(m) > 0 and int(m) < 13: # input month number between 1 and 12
                        if int(m) in [1,3,4,5,7,8,10,12]: # total month day 31
                            if int(d) > 31 or int(d) < 1:
                                messagebox.showinfo(title='Input Day Warning message', message="Input Month is "+m+". Please input day number(DD) between 1 and 31.")
                        elif int(m) in [3,6,9,11]: # total month day 30
                            if int(d) > 30 or int(d) < 1:
                                messagebox.showinfo(title='Input Day Warning message', message="Input Month is "+m+". Please input day number(DD) between 1 and 30.")
                        elif int(m) == 2: # month is Feb
                            if isLeap(int(y)): # leap year Feb has 29 days
                                if int(d) > 29 or int(d) < 1:
                                    messagebox.showinfo(title='Input Day Warning message', message="Input year, "+y+", is leap year. Please note that there are 29 days in February.")
                            else: # normal year Feb has 28 days
                                if int(d) > 28 or int(d) < 1:
                                    messagebox.showinfo(title='Input Day Warning message', message="Please input day number(DD) between 1 and 28. Please note that there are 28 days in February.")
                    else:
                        messagebox.showinfo(title='Input Month Warning message', message="Please input month number(MM) between 1 and 12. For example: 02")
                else:
                    if len(y) != 4:
                        messagebox.showinfo(title='Input Year warning message', message="Please input year number(YYYY). For example: 2018")
                    elif len(m) > 2:
                        messagebox.showinfo(title='Input Month warning message', message="Please input month number(MM). For example: 10")
                    elif len(d) > 2:
                        messagebox.showinfo(title='Input Day warning message', message="Please input day number(DD). For example: 27")
                self.set_year(str(y))
                self.set_month(str(m))
                self.set_day(str(d))
                newWeek = AF.get_weekdays(self.get_year(), self.get_month(), self.get_day())
                self.set_week(newWeek)
                self.clear_labels()
            else:
                messagebox.showinfo(title='Inputs invalid', message="Please ensure you have entered a valid YYYY-MM-DD date.")

        self.dateFrame = LabelFrame(self.mainframe)
        self.dateFrame.grid(row=0, column=1, padx=5, pady=10, sticky=N+W)

        # create Date label
        self.dateLabel = Label(self.dateFrame, text='Input Date', borderwidth=2, relief='groove')
        self.dateLabel.grid(row=0, column=0, padx=4, ipadx=4)
        # create year(YYYY) label and entry box
        self.yLabel = Label(self.dateFrame, text='Year(YYYY)').grid(row=0, column=1, sticky=E)
        self.ytext = StringVar()
        self.yinput = Entry(self.dateFrame, width=5, textvariable = self.ytext).grid(row=0, column=2)
        # create month(MM)label and entry box
        self.mLabel = Label(self.dateFrame, text='Month(MM)').grid(row=0, column=3, sticky=E)
        self.mtext = StringVar()
        self.minput = Entry(self.dateFrame, width=3, textvariable=self.mtext).grid(row=0, column=4)
        # create day(DD) label and entry box
        self.dLabel = Label(self.dateFrame, text='Day(DD)').grid(row=0, column=5, sticky=E)
        self.dtext = StringVar()
        self.dinput = Entry(self.dateFrame, width=3, textvariable = self.dtext).grid(row=0, column=6)
        # create "ENTER" button to jump the week calendar
        self.enterButton = Button(self.dateFrame, text='ENTER', width=4, height=1, command=getDate).grid(row=0, column=7, padx=3)


    def unlock_bind(self, event):
        '''(None) -> None
            A function called by label bind method,
            Unlocking binding relationship with mouse button
        '''
        return


    def clear_labels(self):
        '''(None) -> None
            This function is convenient to call functions in same order repeatedly.
            And function can clear all contents after some calendar actions.
        '''
        for label in self.day_list:
            for i in range(49):
                label[i]['text'] = ''
                label[i]['bg'] = 'white'
                label[i].bind('<Button-1>', self.unlock_bind)
        self.getWeekEvent()
        self.widget_label_labelframe(self.mainframe)


    def info_labelframe(self, mainframe):
        '''(mainframe) -> None
            This info labelframe is build on mainframe,
            Button 'PREV', and 'NEXT' can flip page to previous week or next week.
            'NAME' can change to database name.
        '''
        def getPrevWeek():
            '''(None) -> None
                This function is command function for 'PREV' button,
                it can change a week dates before this week.
            '''
            if len(self.nweek) == 0:
                _p = AF.prev_week(self._week)
                self.set_week(_p)
                self.clear_labels()
            else:
                p = AF.prev_week(self.nweek)
                self.set_week(p)
                self.clear_labels()

        def getNextWeek():
            '''(None) -> None
                This function is command function for 'NEXT' button,
                it can change a week dates after this week.
            '''
            if len(self.nweek) == 0:
                _n = AF.next_week(self._week)
                self.set_week(_n)
                self.clear_labels()
            else:
                n = AF.next_week(self.nweek)
                self.set_week(n)
                self.clear_labels()

        self.infolabelFrame = LabelFrame(self.mainframe)
        self.infolabelFrame.grid(row=1, column=1, padx=5, sticky=W)

        self.prevButton = Button(self.infolabelFrame, text='PREV', width=3, command=getPrevWeek)
        self.prevButton.grid(row=0, column=0)
        self.namelabel = Label(self.infolabelFrame, text='NAME', width=67)
        self.namelabel.grid(row=0, column=1)
        self.nextButton = Button(self.infolabelFrame, text='NEXT', width=3, command=getNextWeek)
        self.nextButton.grid(row=0, column=2)


    def widget_label_labelframe(self, mainframe):
        '''(mainframe) -> None
            This label labelframe is build on mainframe,
            By default, labels can show present week's dates and days.
        '''
        self.cal_labelFrame = LabelFrame(self.mainframe)
        self.cal_labelFrame.grid(row=2, column=1, padx=5, sticky=W)

        # create main calendar label row
        self.timeLabel = Label(self.cal_labelFrame, text='Time', borderwidth=1, relief='solid', width=5, height=2)
        self.timeLabel.grid(row=1, column=1, padx=1)
        i=2
        k=0
        self.dayofweek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.nweek = self.get_week()

        # week dates not change, show present week dates
        if len(self.nweek) == 0:
            self._week = AF.get_this_week()
            for weekday in self.dayofweek:
                self.dayLabel = Label(self.cal_labelFrame, text=self._week, borderwidth=1, relief='solid', width=10, height=2, wraplength=80, anchor='c')
                self.Daylist.append(self.dayLabel)
                self.dayLabel.grid(row=1, column=i, padx=1)
                i+=1
                k+=1
            for n in range(7):
                self.Daylist[n].config(text=self._week[n]+self.dayofweek[n])

        # week dates changed, show changed week dates
        else:
            i=2
            for n in range(len(self.dayofweek)):
                self.dayLabel = Label(self.cal_labelFrame, text=self.nweek[n]+self.dayofweek[n], borderwidth=1, relief='solid', width=10, height=2, wraplength=80, anchor='c')
                self.Daylist.append(self.dayLabel)
                self.dayLabel.grid(row=1, column=i, padx=1)
                i+=1

            for n in range(7):
                self.Daylist[n].config(text=self.nweek[n]+self.dayofweek[n])
                self.dayLabel = Label(self.cal_labelFrame, text=self.nweek[n]+self.dayofweek[n], borderwidth=1, relief='solid', width=10, height=2, wraplength=80, anchor='c')


    def widget_event_labelframe(self, mainframe):
        '''(mainframe) -> None
            This event labelframe is build on mainframe,
            It create calendar in labels.
            Scrollbar connect with canvas, canvas connect with create_window, and create_window connect with labels.
        '''
        self.labelframe = LabelFrame(self.mainframe)
        self.labelframe.grid(row=3, column=1, padx=5, pady=5, sticky=W+N)

        # create a canvas & scrollbar
        self.canvas = Canvas(self.labelframe, width=652, height=640, scrollregion=(0, 0, 596, 1960), highlightthickness=0)
        self.canvas.grid_propagate(False)

        self.sublabelscb = Scrollbar(self.labelframe, orient=VERTICAL)
        self.sublabelscb['command']=self.canvas.yview
        self.canvas['yscrollcommand'] = self.sublabelscb.set
        self.sublabelscb.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

        # calculate 30min event for 24 hours
        event_num = 2*24+1
        time=0
        minute=0

        for i in range(event_num):
            if minute == 0:
                strmin = str(minute)+'0'
            else:
                strmin = str(minute)
            self.timelabel = Label(self.canvas, text=str(time)+':'+strmin, borderwidth=1, bg= 'light grey',relief='solid', width=5, height=2)
            self.timelabel.grid(row=i, column=0, padx=1, pady=1)
            if(minute==30):
                minute=0
                time+=1
            else:
                minute+=30
            self.canvas.create_window(1, i*40, anchor=NW, window=self.timelabel)
        L = Label(self.canvas, text="", borderwidth=1, bg= 'white',relief='solid', width=9, height=2)

        self.li = [self.Sunlist, self.Monlist, self.Tuelist, self.Wedlist, self.Thulist, self.Frilist, self.Satlist]
        for k in range(7):
            for j in range(event_num):
                self.eventlabel = Label(self.canvas, text="", borderwidth=1, bg= 'white',relief='solid', width=10, height=2)
                self.li[k].append(self.eventlabel)
                self.eventlabel.grid(row=j, column=k, padx=1, pady=1)
                # canvas create the "create_window" and put labels on the window
                self.canvas.create_window(k*86+47, j*40, anchor=NW, window=self.eventlabel)


    def getWeekEvent(self):
        '''(None) -> None
            Get whole week event data from .db file,
            then add events into calendar by specific labels.
        '''
        if self.get_database():
            db_name = self.get_database()
            week = self.get_week()
            year = week[0][0:4]
            month = week[0][5:7]
            day = week[0][8:]
            events = CL.get_new_week(db_name, year, month, day)
            for event in events:
                par = partial(self.pop_up_event, event)
                s_time = event.timedate()
                s_time = s_time[0:4]+s_time[5:7]+s_time[8:10]+s_time[11:13]+s_time[14:16]+s_time[17:]
                duration = str(event.duration())
                labels = AF.get_labels(s_time, duration, AF.get_this_week(), self.day_list)
                for label in labels:
                    label['text'] = event.abbreviation()
                    label['bg'] = event.category()
                    label.bind("<Button-1>", par)


    def AddInfo(self):
        ''' (None) -> None
            This pop-up window opened after click 'ADD' button,
            users can add events by fill out information in this window.
        '''
        master = Toplevel()
        self.master = master
        self.master.title("Event Detail Information")
        self.master.geometry('500x615')
        self.master.resizable(width=False, height=False)
        self.inputinfo()


    def getInputInfo(self):
        '''(None) -> None
            get data from entry boxes
            restrict some input format
            use class from CalendarEvent.py to set functions
        '''
        self.name_get = self.event_name_text.get()
        self.abbr_get = self.abbr_text.get()
        self.y_get = self.y_text.get().strip(' ')
        self.m_get = self.m_text.get().strip(' ')
        self.d_get = self.d_text.get().strip(' ')
        self.start_hh_get = self.hh_text.get().strip(' ')
        self.start_mm_get = self.mm_text.get().strip(' ')
        self.dur_hr_get = self.hr_box.get().strip(' ')
        self.dur_minute_get = self.min_box.get().strip(' ')
        self.location_get = self.loc_text.get()
        self.detail_get = self.det_entry.get("1.0", 'end-1c')
        self.color_get = self.select_text.get()
        self.duration = str(int(self.dur_hr_get) * 60 + int(self.dur_minute_get))
        if AF.check_data(self.name_get,self.abbr_get,self.y_get,self.m_get,self.d_get,self.start_hh_get,self.start_mm_get,self.dur_hr_get,self.dur_minute_get,self.location_get,self.detail_get):
            self.Cal_Event = CE.CalendarEvent(self.name_get, self.abbr_get, self.start_hh_get, self.start_mm_get, self.y_get, self.m_get, self.d_get, self.duration, self.detail_get, self.location_get, self.color_get)
            CL.add_event(self.get_database(), self.Cal_Event)
            # show which week is happend this event
            event_week = AF.get_weekdays(self.y_get, self.m_get, self.d_get)
            month = self.m_get
            day = self.d_get
            if int(self.m_get) < 10:
                month = '0'+str(self.m_get)
            if int(self.d_get) < 10:
                day = '0'+str(self.d_get)
            Time = self.y_get+'-'+month+'-'+day
            if Time in AF.get_this_week():
                self.set_week(AF.get_this_week())
                self.getWeekEvent()

            self.master.destroy()
            messagebox.showinfo('Save Prompt',"Following event is saved successfully: \n"+self.name_get)
        else:
            messagebox.showinfo('Check inputs',"Please ensure all required fields are filled out and the date uses correct formatting.")


    def inputinfo(self):
        '''(None) -> None
            This function is command function for 'ADD' button.
            It sets up new window GUI by create
            "name, abbreviation, time, date, duration, description,
            location, and category."
        '''
        self.top_frame = Frame(self.master)
        self.top_frame.grid(row=0, column=0, padx=5, pady=5, sticky=N+W)

        self.event_name_label = Label(self.top_frame, text= "Event Name: * ")
        self.event_name_label.grid(row=0, column=0, sticky=E)
        self.event_name_text = StringVar()
        self.event_name_entry = Entry(self.top_frame, textvariable=self.event_name_text)
        self.event_name_entry.grid(row=0, column=1)
        self.name_hint_label = Label(self.top_frame, text="(Enter the Event Name)")
        self.name_hint_label.grid(row=0, column=2, pady=5, sticky=W)

        self.abbr_label = Label(self.top_frame, text= "Abbreviation: *")
        self.abbr_label.grid(row=1, column=0, pady=5)
        self.abbr_text = StringVar()
        self.abbr_entry = Entry(self.top_frame, textvariable=self.abbr_text)
        self.abbr_entry.grid(row=1, column=1, pady=5)
        self.limit_label = Label(self.top_frame, text="(Limit 10 characters)")
        self.limit_label.grid(row=1, column=2, pady=5, sticky=W)

        self.mid_frame = Frame(self.master)
        self.mid_frame.grid(row=1, column=0, sticky=N+W)

        self.t_label = Label(self.mid_frame, text= "              Date: *")
        self.t_label.grid(row=0, column=0, sticky=E)

        self.y_label = Label(self.mid_frame, text='  Year').grid(row=0, column=1, sticky=E)
        self.y_text = StringVar()
        self.y_input = Entry(self.mid_frame, width=5, textvariable=self.y_text).grid(row=0, column=2)
        self.yhint_label = Label(self.mid_frame, text='(YYYY)').grid(row=0, column=3, sticky=W)

        self.m_label = Label(self.mid_frame, text='   Month').grid(row=0, column=4, sticky=E)
        self.m_text = StringVar()
        self.m_input = Entry(self.mid_frame, width=3, textvariable=self.m_text).grid(row=0, column=5)
        self.mhint_label = Label(self.mid_frame, text='(MM)').grid(row=0, column=6, sticky=W)

        self.d_label = Label(self.mid_frame, text='   Day').grid(row=0, column=7, sticky=E)
        self.d_text = StringVar()
        self.d_input = Entry(self.mid_frame, width=3, textvariable=self.d_text).grid(row=0, column=8)
        self.dhint_label = Label(self.mid_frame, text='(DD)').grid(row=0, column=9, sticky=W)

        self.mid2_frame = Frame(self.master)
        self.mid2_frame.grid(row=2, column=0, padx=5, pady=5, sticky=N+W)

        self.t_label = Label(self.mid2_frame, text="    Start Time: *")
        self.t_label.grid(row=0, column=0)
        self.hh_text = StringVar()
        self.hh_input = Entry(self.mid2_frame, width=3, textvariable=self.hh_text).grid(row=0, column=1)
        self.colon_label = Label(self.mid2_frame, text=" : ").grid(row=0, column=2)
        self.mm_text = StringVar()
        self.mm_input = Entry(self.mid2_frame, width=3, textvariable=self.mm_text).grid(row=0, column=3)
        self.time_hint_label = Label(self.mid2_frame, text="(HH:MM)").grid(row=0, column=4)

        self.mid3_frame = Frame(self.master)
        self.mid3_frame.grid(row=3, column=0, padx=5, pady=5, sticky=N+W)

        self.dur_label = Label(self.mid3_frame, text= "       Duration: *")
        self.dur_label.grid(row=0, column=0)
        self.Hr = ()
        self.Min = ()
        for i in range(25):
            self.Hr += (i,)
        for i in range(60):
            self.Min += (i,)
        self.hr_box = ttk.Combobox(self.mid3_frame, state="readonly", width=5, value=self.Hr)
        self.hr_box.current(0)
        self.hr_box.grid(row=0, column=1)
        self.hr_label = Label(self.mid3_frame, text="(Hr(s))   ").grid(row=0, column=2)
        self.min_box = ttk.Combobox(self.mid3_frame, state="readonly", width=5, value=self.Min)
        self.min_box.current(0)
        self.min_box.grid(row=0, column=3)
        self.min_label = Label(self.mid3_frame, text="(Minute(s))").grid(row=0, column=4)

        self.bot_frame = Frame(self.master)
        self.bot_frame.grid(row=4, column=0, padx=5, pady=5, sticky=N+W)

        self.loc_label = Label(self.bot_frame, text= " Location: ")
        self.loc_label.grid(row=0, column=0, sticky=E)
        self.loc_text  = StringVar()
        self.loc_entry = Entry(self.bot_frame, textvariable=self.loc_text, width=40)
        self.loc_entry.grid(row=0, column=1, sticky=W)

        self.det_label = Label(self.bot_frame, text= "Detail: ")
        self.det_label.grid(row=1, column=0, pady=10, sticky=N)
        self.tbox_frame = LabelFrame(self.bot_frame)
        self.tbox_frame.grid(row=1, column=1, pady=10)
        self.det_entry = Text(self.tbox_frame, width=50, height= 13)
        self.det_entry.grid(row=0, column=0)

        self.categories = [("None", "White"), ("Work", "Blue"), ("Study", "Yellow"), ("Chore", "light green"), ("Leisure", "orange")]
        self.cat_frame = Frame(self.master)
        self.cat_frame.grid(row=5, column=0, padx=10, pady=5, sticky=N+W)
        self.cat_label = Label(self.cat_frame, text="Category: ").pack(side=LEFT)
        self.select_text = StringVar()
        self.select_text.set("White")
        for num, cat in enumerate(self.categories):
            Radiobutton(self.cat_frame, text=cat[0], padx=5, variable=self.select_text, value=cat[1]).pack(anchor=W)
        self.require_field_label = Label(self.master, text="* : required fields").place(x=10, y=580)

        self.button_frame = Frame(self.master)
        self.button_frame.grid(row=6, column=0, padx=10, pady=5)
        self.save_button = Button(self.button_frame, text="Save", command=self.getInputInfo)
        self.save_button.grid(row=0, column=0)


    def pop_up_event(self, event, *args):
        ''' (None) -> None
            This pop-up window is to show information about added events,
            users can change information on this window.
        '''
        timedate = event.timedate()
        self.set_fulldatetime(timedate)
        self.popup_name = event.event()
        self.popup_abbr = event.abbreviation()
        self.popup_year = event.year()
        self.popup_month = event.month()
        self.popup_day = event.day()
        self.popup_hr = event.hour()
        self.popup_min = event.minute()
        self.popup_dur_hr = event.duration() // 60
        self.popup_dur_mim = event.duration() % 60
        self.popup_location = event.place()
        self.popup_detail = event.detail()
        self.popup_cat = event.category()
        weekday = AF.get_weekdays(self.popup_year, self.popup_year, self.popup_day)
        start = timedate[0:4]+timedate[5:7]+timedate[8:10]+timedate[11:13]+timedate[14:16]+timedate[17:]
        self.event_labels = AF.get_labels(start, event.duration(), weekday, self.day_list)
        # setup pop-up window
        event_window = Toplevel()
        self.event_window = event_window
        self.event_window.title("Show Event Information")
        self.event_window.geometry('500x615')
        self.event_window.resizable(width=False, height=False)
        self.pop_up_info()
    

    def update_pop_up_Info(self):
        # update_event(db, event, dt)
        pass

    def del_event(self):
        '''(None) -> None
            This function is command function for 'DELETE' button.
            User click button can delete event from calendar,
            also delete data from database
        '''
        db = self.get_database()
        dt = self.get_fulldatetime()
        # delete event data from database
        CL.delete_event(db, dt)
        # update events in the week
        self.getWeekEvent()
        # clear deleted event labels and unlock labels bind relations
        for label in self.event_labels:
            label['text'] = ''
            label['bg'] = 'white'
            label.bind('<Button-1>', self.unlock_bind)
        # update calendar frame
        self.widget_label_labelframe(self.mainframe)
        # close the pop-up window
        self.event_window.destroy()
        # hint user delete event successfully
        messagebox.showinfo('Delete Prompt',"Following event is deleted successfully: \n"+self.popup_name)


    def pop_up_info(self):
        self.top_frame = Frame(self.event_window)
        self.top_frame.grid(row=0, column=0, padx=5, pady=5, sticky=N+W)

        self.event_name_label = Label(self.top_frame, text= "Event Name: * ")
        self.event_name_label.grid(row=0, column=0, sticky=E)
        self.event_name_text = StringVar(self.top_frame, value=self.popup_name)
        self.event_name_entry = Entry(self.top_frame, textvariable=self.event_name_text)
        self.event_name_entry.grid(row=0, column=1)
        self.name_hint_label = Label(self.top_frame, text="(Enter the Event Name)")
        self.name_hint_label.grid(row=0, column=2, pady=5, sticky=W)

        self.abbr_label = Label(self.top_frame, text= "Abbreviation: *")
        self.abbr_label.grid(row=1, column=0, pady=5)
        self.abbr_text = StringVar(self.top_frame, value=self.popup_abbr)
        self.abbr_entry = Entry(self.top_frame, textvariable=self.abbr_text)
        self.abbr_entry.grid(row=1, column=1, pady=5)
        self.limit_label = Label(self.top_frame, text="(Limit 10 characters)")
        self.limit_label.grid(row=1, column=2, pady=5, sticky=W)

        self.mid_frame = Frame(self.event_window)
        self.mid_frame.grid(row=1, column=0, sticky=N+W)

        self.t_label = Label(self.mid_frame, text= "              Date: *")
        self.t_label.grid(row=0, column=0, sticky=E)

        self.y_label = Label(self.mid_frame, text='  Year').grid(row=0, column=1, sticky=E)
        self.y_text = StringVar(self.mid_frame, value=self.popup_year)
        # self.y_text.trace('w', self.limitsize)
        self.y_input = Entry(self.mid_frame, width=5, textvariable=self.y_text).grid(row=0, column=2)
        self.yhint_label = Label(self.mid_frame, text='(YYYY)').grid(row=0, column=3, sticky=W)

        self.m_label = Label(self.mid_frame, text='   Month').grid(row=0, column=4, sticky=E)
        self.m_text = StringVar(self.mid_frame, value=self.popup_month)
        self.m_input = Entry(self.mid_frame, width=3, textvariable=self.m_text).grid(row=0, column=5)
        self.mhint_label = Label(self.mid_frame, text='(MM)').grid(row=0, column=6, sticky=W)

        self.d_label = Label(self.mid_frame, text='   Day').grid(row=0, column=7, sticky=E)
        self.d_text = StringVar(self.mid_frame, value=self.popup_day)
        self.d_input = Entry(self.mid_frame, width=3, textvariable=self.d_text).grid(row=0, column=8)
        self.dhint_label = Label(self.mid_frame, text='(DD)').grid(row=0, column=9, sticky=W)

        self.mid2_frame = Frame(self.event_window)
        self.mid2_frame.grid(row=2, column=0, padx=5, pady=5, sticky=N+W)

        self.t_label = Label(self.mid2_frame, text="    Start Time: *")
        self.t_label.grid(row=0, column=0)
        self.hh_text = StringVar(self.mid2_frame, value=self.popup_hr)
        self.hh_input = Entry(self.mid2_frame, width=3, textvariable=self.hh_text).grid(row=0, column=1)
        self.colon_label = Label(self.mid2_frame, text=" : ").grid(row=0, column=2)
        self.mm_text = StringVar(self.mid_frame, value=self.popup_min)
        self.mm_input = Entry(self.mid2_frame, width=3, textvariable=self.mm_text).grid(row=0, column=3)
        self.time_hint_label = Label(self.mid2_frame, text="(HH:MM)").grid(row=0, column=4)

        self.mid3_frame = Frame(self.event_window)
        self.mid3_frame.grid(row=3, column=0, padx=5, pady=5, sticky=N+W)

        self.dur_label = Label(self.mid3_frame, text= "       Duration: *")
        self.dur_label.grid(row=0, column=0)
        self.Hr = ()
        self.Min = ()
        for i in range(25):
            self.Hr += (i,)
        for i in range(60):
            self.Min += (i,)
        self.hr_box = ttk.Combobox(self.mid3_frame, state="readonly", width=5, value=self.Hr)
        self.hr_box.current(self.popup_dur_hr)
        self.hr_box.grid(row=0, column=1)
        self.hr_label = Label(self.mid3_frame, text="(Hr(s))   ").grid(row=0, column=2)
        self.min_box = ttk.Combobox(self.mid3_frame, state="readonly", width=5, value=self.Min)
        self.min_box.current(self.popup_dur_mim)
        self.min_box.grid(row=0, column=3)
        self.min_label = Label(self.mid3_frame, text="(Minute(s))").grid(row=0, column=4)

        self.bot_frame = Frame(self.event_window)
        self.bot_frame.grid(row=4, column=0, padx=5, pady=5, sticky=N+W)

        self.loc_label = Label(self.bot_frame, text= " Location: ")
        self.loc_label.grid(row=0, column=0, sticky=E)
        self.loc_text  = StringVar(self.bot_frame, value=self.popup_location)
        self.loc_entry = Entry(self.bot_frame, textvariable=self.loc_text, width=40)
        self.loc_entry.grid(row=0, column=1, sticky=W)

        self.det_label = Label(self.bot_frame, text= "Detail: ")
        self.det_label.grid(row=1, column=0, pady=10, sticky=N)
        self.tbox_frame = LabelFrame(self.bot_frame)
        self.tbox_frame.grid(row=1, column=1, pady=10)
        self.det_entry = Text(self.tbox_frame, width=50, height= 13)
        self.det_entry.insert(END, self.popup_detail)
        self.det_entry.grid(row=0, column=0)

        self.categories = [("None", "White"), ("Work", "Blue"), ("Study", "Yellow"), ("Chore", "light green"), ("Leisure", "orange")]
        self.cat_frame = Frame(self.event_window)
        self.cat_frame.grid(row=5, column=0, padx=10, pady=5, sticky=N+W)
        self.cat_label = Label(self.cat_frame, text="Category: ").pack(side=LEFT)
        self.select_text = StringVar()
        self.select_text.set(self.popup_cat)
        for num, cat in enumerate(self.categories):
            Radiobutton(self.cat_frame, text=cat[0], padx=5, variable=self.select_text, value=cat[1]).pack(anchor=W)
        self.require_field_label = Label(self.event_window, text="* : required fields").place(x=10, y=580)

        self.button_frame = Frame(self.event_window)
        self.button_frame.grid(row=6, column=0, padx=10, pady=5)
        self.update_button = Button(self.button_frame, text="UPDATE", command=self.update_pop_up_Info)
        self.update_button.grid(row=0, column=0)
        self.delete_button = Button(self.button_frame, text="DELETE", command=self.del_event)
        self.delete_button.grid(row=0, column=1)


def closeWindow():
    '''(None) -> QUIT
        Hint for user when click close button, 'x', upper left corner of application.
    '''
    if builtins.unsaved == False:
        ans = messagebox.askyesno('Save Events', 'You did not save your events, would you like to quit?')
        if ans:
            root.destroy()
    else:
        root.destroy()


if __name__ == '__main__':
        
    def exception_callback(self, exception, value, trace):
        '''This function overrides the tk report_callback_exception function to display an error window.'''
        traceback.print_exception(exception, value, trace) #Should remove this line before submitting. This line prints the exception. Useful for debugging, but if left in it will make the program look even more buggy than it is when run.
        messagebox.showerror("Error!",message=str(value))

    Tk.report_callback_exception = exception_callback #This is the line that makes exception_callback actually get used
    
    root = Tk()
    root.resizable(width=False, height=False)
    root.title("Calendar")
    root.geometry('810x810')
    builtins.unsaved == True
    root.protocol('WM_DELETE_WINDOW', closeWindow)
    Calendar(root)
    root.mainloop()
