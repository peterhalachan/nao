#Main file of the TellTheResult program
import sys #imported modules which are used to ren the program
import time
import TellTheResult
from naoqi import ALBroker

ip = "192.168.0.106" #ip address of the robot

myBroker = ALBroker("myBroker", "0.0.0.0", 0, ip, 9559) #We need this broker to be able to construct.NAOqi modules and subscribe to other modules. The broker must stay alive until the program exists
RecognizeResult = TellTheResult.RecognizeModule("RecognizeResult") #instantiation of the TellTheResult class which is called from the imported TellTheResult file

while True:
    time.sleep(1) #suspends execution of the current thread for one second

myBroker.shutdown() #the program is shut down
sys.exit(0) #exit from python which gives the exit status one
