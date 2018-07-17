from CalendarEvent import *
from CalendarLogic import *

# load or make new .db
calendar = load_calendar_model('SethTempleCalendar.db')

# make events
e1 = CalendarEvent('Software Methodologies', 'CIS 422', 10, 0, 2018, 4, 24, 90, 'This course is taught by Anthony Hornof. We learn about software engineering.', 'Price Science Commons', 'school' )
e2 = CalendarEvent('Software Methodologies', 'CIS 422', 10, 0, 2018, 4, 26, 90, 'This course is taught by Anthony Hornof. We learn about software engineering.', 'Price Science Commons', 'school' )
e3 = CalendarEvent('Fickas Meeting', 'RULE', 14, 0, 2018, 4, 23, 30, 'I meet with Jason and Steve to talk about our NN.',
                  'Deschutes 3rd Floor', 'work')
e4 = CalendarEvent('Sinclair Meeting', 'Thesis', 14, 0, 2018, 4, 26, 60, 'I meet with Chris to discuss my thesis defense.',
                  'Deady 2nd Floor Mezzanine', 'school')
e5 = CalendarEvent('Soccer Practice', 'Soccer', 6, 0, 2018, 4, 23, 120, 'Early morning practice prior to California showcase',
                  'Rec Field #2', 'leisure')
e6 = CalendarEvent('Soccer Practice', 'Soccer', 6, 0, 2018, 4, 25, 120, 'Early morning practice prior to California showcase',
                  'Rec Field #2', 'leisure')
e7 = CalendarEvent('Grocery Shopping', 'Groceries', 15, 0, 2018, 4, 23, 30, 'I got some trash bags and bell peppers.',
                  '18th and Willamete', 'chore')
e9 = CalendarEvent('Drive to California', 'Drive', 16, 0, 2018, 4, 26, 480, 'Soccer team drives to Elk Grove, CA.',
                  'Mac Court', 'leisure')
e10 = CalendarEvent('Fickas Meeting', 'RULE', 14, 0, 2018, 4, 16, 30, 'I meet with Jason and Steve to talk about our NN.',
                  'Deschutes 3rd Floor', 'work')
e11 = CalendarEvent('Software Methodologies', 'CIS 422', 10, 0, 2018, 4, 17, 90, 'This course is taught by Anthony Hornof. We learn about software engineering.', 'Price Science Commons', 'school' )
e12 = CalendarEvent('Software Methodologies', 'CIS 422', 10, 0, 2018, 4, 19, 90, 'This course is taught by Anthony Hornof. We learn about software engineering.', 'Price Science Commons', 'school' )
e13 = CalendarEvent('Software Methodologies', 'CIS 422', 10, 0, 2018, 5, 1, 90, 'This course is taught by Anthony Hornof. We learn about software engineering.', 'Price Science Commons', 'school' )
e14 = CalendarEvent('Software Methodologies', 'CIS 422', 10, 0, 2018, 5, 3, 90, 'This course is taught by Anthony Hornof. We learn about software engineering.', 'Price Science Commons', 'school' )

# add events
add_event(calendar, e1)
add_event(calendar, e2)
add_event(calendar, e3)
add_event(calendar, e4)
add_event(calendar, e5)
add_event(calendar, e6)
add_event(calendar, e7)
add_event(calendar, e9)
print(Calendar.unsaved)

save_changes(calendar)
print(Calendar.unsaved)

add_event(calendar, e10)
add_event(calendar, e11)
add_event(calendar, e12)
print(Calendar.unsaved)

save_changes(calendar)
print(Calendar.unsaved)

add_event(calendar, e13)
add_event(calendar, e14)
print(Calendar.unsaved)

save_changes(calendar)
print(Calendar.unsaved)

# Raises ValueError
#add_event(calendar, e1)

# Small test of functions
backup_calendar(calendar)
print(get_new_week(calendar, 2018, 5, 2))
print(get_new_week(calendar, 2018, 4, 17))

ne4 = CalendarEvent('Sinclair Meeting', 'Thesis', 13, 0, 2018, 4, 26, 30, 'I meet with Chris to discuss my thesis defense.',
                  'Deady 2nd Floor Mezzanine', 'school')
update_event(calendar, ne4, '2018-04-26 14:00:00')
print(Calendar.unsaved)

save_changes(calendar)
print(Calendar.unsaved)

ne4 = CalendarEvent('Sinclair Meeting', 'Thesis', 13, 0, 2018, 4, 26, 60, 'I meet with Chris to discuss my thesis defense.',
                  'Deady 2nd Floor Mezzanine', 'school')
update_event(calendar, ne4, '2018-04-26 13:00:00')
print(Calendar.unsaved)

save_changes(calendar)
print(Calendar.unsaved)
