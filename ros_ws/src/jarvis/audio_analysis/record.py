#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import pyaudio
import math
import struct
import wave
import time
import os
import subprocess
import audioop
import numpy as np

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 3
if not os.path.exists('/home/mady/Music/recordings'):
    os.mkdir('/home/mady/Music/recordings')
f_name_directory = r'/home/mady/Music/recordings'
Threshold = rospy.get_param('Audio_analysis/ambient_noise_rms')
        
class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000
    @staticmethod
    def variance(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)
        var = np.var(np.array(shorts)/327.68)
        return abs(var)

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    output=True,
                                    frames_per_buffer=chunk)

    def record(self):
        print('Audio detected, recording begun')
        rec = []
        global Threshold
        start_time=round(time.time())
        current = start_time
        end = round(time.time()) + TIMEOUT_LENGTH
        while current <= end:
            data = self.stream.read(chunk)
            if a.variance(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH
            #if self.rms(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH
            current = round(time.time())
            rec.append(data)
            print(current-start_time)
            #if current-start_time > 20:
        if current - start_time < 4:
            # print("rms_value",self.rms(data))
            # print("Threshold", Threshold)
            # Threshold+=2*Threshold
            # rospy.set_param('Audio_analysis/ambient_noise_rms',Threshold)
            #time_up=True
            print("sorry considered as noise")
            #break
        else: 
            #time_up = False
            self.write(b''.join(rec))

        # if not time_up:
        #     self.write(b''.join(rec))

    def write(self, recording):
        n_files = len(os.listdir(f_name_directory))
        if n_files>3:
            delete_files(f_name_directory)
            n_files=0
        filename = os.path.join(f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        #Threshold_update()
        print('Written to file: {}'.format(filename))
        print('Returning to listening')


def delete_files(addr):
    for file in os.listdir(addr):
        os.remove(addr + '/' +file)
    
def Threshold_update():
    input = a.stream.read(chunk)
    global Threshold 
    Threshold = 4*a.rms(input) #audioop.rms(input,2)*0.5
    rospy.set_param('Audio_analysis/ambient_noise_rms',Threshold)

def noise_detection():
    print('please wait 5 secs for noise calibration..')
    for i in range(1,20):
        Threshold_update()
        time.sleep(0.5)
        print(Threshold)
    print('calibration done.. Thankyou')

def find_thres():
    global Threshold
    print('please wait 5 secs for noise calibration..')
    arr = []
    for i in range(1,20):
        input = a.stream.read(chunk)
        vary = a.variance(input)
        arr.append(vary)
        time.sleep(0.1)
    Threshold = 5*np.mean(arr)
    print('calibration done.. Thankyou')

a = Recorder()
def talker():
    pub = rospy.Publisher('Audio_analysis',String,queue_size=5)
    rospy.init_node('recorder')
    #noise_detection()
    find_thres()
    input = a.stream.read(chunk)

    while not rospy.is_shutdown():
        global Threshold
        input = a.stream.read(chunk)
        #rms_val = a.rms(input)
        change = a.variance(input)
        #rms_val = audioop.rms(input,2)
        #if rms_val > Threshold:
        if change > Threshold:
            print("change",change)
            print("Threshold", Threshold)
            a.record()
            name = len(os.listdir(f_name_directory))
            pub.publish('Audio_recorded '+str(name-1))
        #time.sleep(0.5)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
