#### Idea is to create assitant robot on linux platform using ROS
Current state: 
A ros publisher node which reccords audio on once sound crosses threshold is created.
A text to speech converter node in ROS which subscribes to recorder and converts audio to text once recording finished.
A calender event program in python which takes the last line of text file and analyse for any calander event and
creates a calander event compatible with calcurse event format.

Planning To:
1. Make conversion as an action server with text as goal
2. Call conversion action as call back function in speech2txt node.
3. Make a jarvis listner node and subscribe to recording node. on event if conversion status is success then do call back function. call back function request text analysis service. Based on result give goals to action servers.
4. Let text analysis be the service which catagorises the voice command by finding key words and returns key words.
5. Let Event_writer be an action server triggered by jarvis upon Remind, with goal to write text into event file and publish.
6. Let event_manager be a service which is initiated by jarvis on start. And event_manager service will continously run to monitor events and call text speech action
7. Let text to speech be another action which can be called with goal of text to be spoken which could be called by any other action.

TODO: Ambient noise calibration in record node need to be included
