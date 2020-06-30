#!/usr/bin/env python

'''
Finds time in all these formats
half an hour, 1:05 p.m. one and half hour, 3 hours 15 minutes, 2 hours, 15 minuites

todo: Find all times, find every half an hour, find weekly etc, 'by 430' wont work. pm or am is must
Use ros string and see if somethings else can be done
'''
import rospy
from std_msgs.msg import String
import os
import re
import datetime
import time
import calendar
#import pdb

# To find name of the day
def findDay(date): 
    born = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    return (calendar.day_name[born]) 

# function to find time
def find_time(last_line,tomorrow=False):
    hours = 0
    mins = 0
    match=None
    #pdb.set_trace()
    match = hour.search(last_line)
    if match:
        hours = match.group()[:-5]
        last_line = last_line.replace(match.group(),'')
        #print(match,hours)

    match=None
    match = min.search(last_line)
    if match:
        mins = match.group()[:-7]
        #print(match.group())
        last_line = last_line.replace(match.group(),'')
        #print(match,mins)

    match=None
    match = AM_time.search(last_line)
    if match:
        strs = match.group()[:-5]
        hours,mins = strs.split(':')
        if hours=='12':
            hours = '00'
        last_line = last_line.replace(match.group(),'')
        #print(match,hours,mins)

    match=None
    match = PM_time.search(last_line)
    if match:
        strs = match.group()[:-5]
        hours,mins = strs.split(':')
        if hours=='12':
            hours = '00'
        hours = int(hours)+12
        #hours = str(hours)
        last_line = last_line.replace(match.group(),'')
        #print(match,hours,mins)

    if 'half an hour' in last_line:
        hrs = '00'
        mns = '30'
        current_time = time.strftime("%H %M")
        hours,mins = current_time.split()
        hours = int(hours)+int(hrs)
        mins = int(mins) + int(mns)
        if mins>60:
            hours+=1
        if hours>23:
            hours=0
            tomorrow=True
        last_line = last_line.replace('half an hour','')
        #print(hours,mins)

    if 'one and half hour' in last_line:
        hrs = '01'
        mns = '30'
        current_time = time.strftime("%H %M")
        hours,mins = current_time.split()
        hours = int(hours)+int(hrs)
        mins = int(mins) + int(mns)
        if mins>59:
            hours+=1
        if hours>23:
            hours=0
            tomorrow=True
        last_line = last_line.replace('one and half hour','')
        #print(hours,mins)
    
    if not hours and mins:
        current_time = time.strftime("%H %M")
        hours,mns = current_time.split()
        mins = int(mins) + int(mns)
    if not mins and hours:
        current_time = time.strftime("%H %M")
        hrs,mins = current_time.split()
        hours = int(hours) + int(hrs)
    if not hours and not mins:
        hours = 9; mins =0
    return int(hours),int(mins),tomorrow,last_line

# function to find date
def find_date(last_line,tomorrow):
    # find months and days in words and convert to numbers
    #pdb.set_trace()
    words = last_line.split()
    day = 0; month=0
    # for format like remind on 13th august
    for word in words:
        if word in monthToNum:
            month = monthToNum[word]
            ex = '[0-9].*?'+word
            match  = re.search(ex,last_line)
            if match:
                day = re.search(r'\d+', match.group()).group()
                last_line = last_line.replace(match.group(),'')
            match  = re.search(ex,last_line)
            if match:    
                day = re.search(r'\d+', match.group()).group()
                last_line = last_line.replace(match.group(),'')
    if not day and not month:
        # for with in week reminders like remind me on monday
        dt = None
        for word in words:
            if word in dayTonum:    
                day = dayTonum[word]
                print(day)
                last_line = last_line.replace(word,'')
                dt = datetime.datetime.today()
                date = dt.strftime("%d %m %Y")
                weekday = findDay(date).lower()
                to_day = dayTonum[weekday]
                gap = day-to_day
                if gap<=0 or 'next' in words:
                    gap = 7+gap
                dt = datetime.datetime.today()+datetime.timedelta(days=gap)
                #adust number with current date
        if 'tomorrow' in last_line or tomorrow:
            dt = datetime.datetime.today()+datetime.timedelta(days=1)
            last_line = last_line.replace('tomorrow','') 
        elif 'day after tomorrow' in last_line:
            dt = datetime.datetime.today()+datetime.timedelta(days=2)
            last_line = last_line.replace('day after tomorrow','')
        #elif 'next week' in last_line:
            #dt = datetime.datetime.today()+datetime.timedelta(weeks=1)
            #last_line = last_line.replace('next week','')
        elif dt is None:
            dt = datetime.datetime.today()
        date = dt.strftime("%Y %m %d")
        year,month,day = date.split()

        if 'next month' in last_line:
            month = int(month)+1
            last_line = last_line.replace('next month','')
    else:
        dt = datetime.datetime.today()
        year = dt.strftime("%Y")
        if month is None:
            year = dt.strftime("%m")

    return int(year),int(month), int(day),last_line

def cleanup(msg):
    msg = msg.replace('by','')
    msg = msg.replace('s','')
    msg = msg.replace('jarvis','')
    return msg

### regex objects
hour = re.compile('\\d+ hour')
min = re.compile('\\d+ minute')
AM_time = re.compile('[0-9]+:[0-9]+ a.m.')
PM_time = re.compile('[0-9]+:[0-9]+ p.m.')

# month to number change
monthToNum ={'january' : 1,
            'february' : 2,
            'march' : 3,
            'april' : 4,
            'may' : 5,
            'june' : 6,
            'july' : 7,
            'august' : 8,
            'september': 9, 
            'october' : 10,
            'november' : 11,
            'december' : 12}
dayTonum = {'monday':1,
            'tuesday':2,
            'wednesday':3,
            'thursday':4,
            'friday':5,
            'saturday':6,
            'sunday':7}
def callback(arg):
    if arg.data == "audio_converted":  
        # Open and read last line of file
        f = r'/home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/data/speech2txt.txt'
        #calendar = r'/home/mady/.calcurse/apts'
        speech2txt = open(f,"r+")
        lines = speech2txt.readlines()
        speech2txt.close()
        last_line = lines[-1]
        del lines
        speech2txt.close()
        last_line= last_line.lower()
        # open file and search for time, date and create event and write to calander
        print(last_line)
        print("")
        #pdb.set_trace()
        if 'remind' in last_line:
            tomorrow = False
            hours,mins,tomorrow,last_line = find_time(last_line,tomorrow)
            year,month,date,last_line = find_date(last_line,tomorrow)
            #last_line = cleanup(last_line)
            details = [year,month,date,hours,mins]
            event = "".join(map(str,details))
            event = event+'-->'+last_line
            f = r'/home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/data/calander.txt'
            written = False
            attempt = 0
            while not written and attempt<3: 
                try:
                    calander = open(f, "a")
                    calander.write(event)
                    calander.close()
                    written = True
                    attempt=3
                except IOError:
                    attempt+=1
                    written=False
                    if attempt ==3:
                        print('calender file is not available')
                    pass
        else:
            print('some_other_message')
    return

rospy.init_node('event_finder')
sub = rospy.Subscriber('Audio_analysis',String,callback)
rospy.spin()