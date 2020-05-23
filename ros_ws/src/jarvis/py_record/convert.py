#!/usr/bin/env python

# Converter the audio files recorded to text files

import rospy
from std_msgs.msg import String
import os
#import shutil
import speech_recognition as sr 


# Initialize the recognizer  
r = sr.Recognizer() 


audio_directory = r'/home/mady/Music/recordings'
text_file = r'/home/mady/MEGA/mady/courses/learn_ros_python/ros_ws/src/jarvis/speech2txt.txt'


def callback(file_name):
    wav = file_name.data + ".wav"
    print(wav)
    wavename = os.path.join(audio_directory, wav)     
    record = sr.AudioFile(wavename) 
    # Exception handling to handle 
    # exceptions at the runtime 
    try: 
        # use the microphone as source for input. 
        with record as source: 
            audio = r.record(source)
            # Using ggogle to recognize audio 
            print("converting..")
            MyText = r.recognize_google(audio) 
            file1 = open(text_file,'a')
            file1.write(MyText + " \n")
            file1.close()
            file1 = open(text_file,"r+")
            print(file1.read())
            file1.close()
            # Move file to archives
            #shutil.move(wavename,archive_dir)  
            
    except sr.RequestError as e: 
        print("Could not request results; {0}".format(e)) 
        
    except sr.UnknownValueError: 
        print("unknown error occured") 

rospy.init_node('audio_converter')

sub = rospy.Subscriber('py_speech',String,callback)

rospy.spin()