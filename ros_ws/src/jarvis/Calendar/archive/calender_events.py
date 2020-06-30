'''
TODO - recurrin items not done, statements like rmind me after a week, or month or n weeks or an year is not done
230 will be taken as 2h 30 m by default even thought it is money
'''

import re
from w2n_full_text import my_w2n
from datetime import date
import time
#word to number conversion object
word2num = my_w2n()

### regex objects
h = re.compile('\\d+ h')
m = re.compile('\\d+ m')
h_m_by = re.compile('\\d+ \\d+ pm')
by_h = re.compile('by \\d+')
n_days = re.compile('\\d+ days')
n_months = re.compile('\\d+ months')
#####

speech2txt = r'/home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/data/speech2txt.txt'
my_file = open(speech2txt,"r+")
found =False
tommorow = False
for last_line in my_file:
    last_line = last_line.lower()
    pass

if 'remind' in last_line:
    words,found,short = word2num.find_time(last_line)
if found:
    # hours = hour.search(s)
    # 

    print(words)
    print("")
    print(last_line)
    s = " "
    s = s.join(words)
    print(s)
    hour = h.search(s)
    min = m.search(s)
    s = s.replace('remind','')
    s = s.replace(' me ','')

    

    if hour is None and min is None:
        h_m = h_m_by.search(s)
        if h_m:
            hours = h_m.group().split()[0]
            mins = h_m.group().split()[1]
            s = s.replace(h_m.group(),'')
        _h = by_h.search(s)
        if _h:
            hours = _h.group()[3:]
            mins = '00'
            s = s.replace(_h.group(),'')

    else:
        if hour is None:
            hours= 0
        else: 
            hours = hour.group()[:-1]
            s = s.replace(hour.group(),'')

        if min is None:
            mins = 0
        else: 
            mins = min.group()[:-1]
            s = s.replace(min.group(),'')
    
    if 'pm' in s:
        s = s.replace('pm','')
        if int(hours) != 12:
            hours = str(int(hours)+12)
        
    today = date.today()
    # mm/dd/y
    current_date = today.strftime("%m/%d/%y")
    current_time = time.strftime("%H:%M")
    day = current_date[3:5]
    month = current_date[0:2]
    year = current_date[-2:]
    print(day,month,year)
    if 'tommorow' in s:
        tommorow = True
        s = s.replace('tommorow','')
    if short:
        hours = int(hours)
        mins = int(mins)
        event_time_m = int(current_time[3:5]) + mins
        if event_time_m > 60:
            hours+=1
            event_time_m-=60
            event_time_m = str(event_time_m) 
        event_time_h = int(current_time[0:2]) + hours
        if event_time_h >=24: 
            event_time_h -=24
            event_time_h = str(event_time_h)
            tommorow = True
    else:
        event_time_h = hours
        event_time_m  = mins

    event_time = str(event_time_h) + ':' + str(event_time_m) 
    if tommorow:
        day = str(int(day)+1)
    if 'day after tommorow' in s:
        day = str(int(day)+2)
        s = s.replace('day_after_tommorow','')
    if 'next month' in s:
        month = str(int(month)+1)
        s = s.replace('next_month','')
    if 'next year' in s:
        year = str(int(year)+1)
        s = s.replace('next year','')
    # if n_days.search(s):
    #     day = int(day)+ int(n_days.search(s).group())
    # if n_months.search(s):
    #     day = int(day)+ int(n_months.search(s).group())
    event_date = month + '/'+ day + '/' + year
     ## find remainder
    if 'am' in s:
        s = s.replace('am','')
    if 'by' in s:
        s = s.replace('by','')
    if 'hour' in s:
        s = s.replace('hour','')
    print(s)
    
    event = current_date + ' @ '+ current_time + ' -> ' + event_date + ' @ ' + event_time + '|' + s + ' ' + s
    print(event)
else: print("no remind found in text")



