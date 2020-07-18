#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import subprocess
from datetime import datetime
import sys
import os
import time
#import pdb

def get(command):
    return subprocess.check_output(command).decode("utf-8")

def convert(t):
    # convert set time into a calculate- able time
    return [int(n) for n in t.split(":")]

def calc_diff(t_curr, t_event):
    # calculate time span
    diff_hr = (t_event[0] - t_curr[0])*60
    diff_m = t_event[1] - t_curr[1]
    return diff_hr + diff_m

def update(events):
    # clean up "done" this must delete line of text if it is not repeating alarm.
    f = open(my_file, "w")
    f.writelines( list( "%s\n" % item for item in events ) )
    f.close()

def show_time(s):
    # show scheduled event
    subprocess.call(["notify-send", s])
    speak_cmd = "espeak \"{}\" ".format(s)
    os.system(speak_cmd)

def cleanup(msg):
    msg = msg.replace(' by ','')
    msg = msg.replace(' s ','')
    msg = msg.replace(' jarvis ','')
    msg = msg.replace(' in ','')
    msg = msg.replace(' me ',' you ')
    msg = msg.replace(' i ',' you ')
    msg = msg.replace(' on ','')
    return msg

cal_dict = {}
Done=[]
#pdb.set_trace()
pub = rospy.Publisher('Calendar',String,queue_size=5)
rospy.init_node('calendar_monitor')
while not rospy.is_shutdown():

    my_file = r'/home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/data/calander.txt'
    #calendar = r'/home/mady/.calcurse/apts'
    calendar= open(my_file, "r")
    events = calendar.readlines()
    calendar.close()
    # while("\n" in events) : 
    #     events.remove("\n")
    # while(" \n" in events) : 
    #     events.remove(" \n")

    dt = datetime.now()
    now = dt.strftime("%Y %m %d %H %M")
    data = [int(s) for s in now.split()]
    now = "".join(map(str,data))
    line = 0
    if events:
        for event in events:
        # arrange event data:    # calendar file will have text in format year-month-date-hours-mins-->message-->repeat-with text(daily, weekly, monthly, yearly, hourly -number)    
            line +=1
            details = event.split('-->')
            if len(details)==2:
                date_n_time = details[0]
                message = details[1]
                #message = cleanup(message)
                    
                #repeat = details[2]
                cal_dict.update({date_n_time:[line,message]})  # todo: if same date and time found append the key value dont update
        # run notifications
        if now in cal_dict:
            message = cal_dict[now][1]
            #line = cal_dict[now][0]
            show_time(message)
            #Done.append(line)     
            # clean up events
            events.pop(line-1) # remove the line item from list, by line number, starts from 0
            update(events)
            pub.publish(message)

    time.sleep(30)

'''
stop_sound = False
while not stop_sound:
     process = subprocess.Popen(["afplay", "beep.wav"], shell=False)
     if stop_sound:
         process.kill()
'''