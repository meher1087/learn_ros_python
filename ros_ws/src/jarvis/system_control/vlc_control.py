# #!/usr/bin/env python

'''
This is action server to control vlc player.
todo: find out how to start and stop vlc using python commands conditionally
we use vlc-ctrl module which can be installed using pip3 vlc-ctrl

vlc-ctrl pause
vlc-ctrl play -p /home/user/music
vlc-ctrl volume +10%
vlc-ctrl volume +0.1

Quit when return code of “command” is 0, retrying the command at most 5 times at 30s intervals and fade out in 10s:
vlc-ctrl quit -c command -r 5,30 -f 10

track info
vlc-ctrl info

more commands
vlc-ctrl -h
'''
import subprocess

import vlc_control

