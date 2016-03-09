#TellTheResult is executed by the Main.py file
from naoqi import ALProxy #from naoqi module ALProxy is imported
from naoqi import ALModule #from naoqi module ALModule is imported
import random #random module is imported

ip = "192.168.0.106" #ip address od robot

class RecognizeModule(ALModule): #this class inherits from the ALModule
    def __init__(self, name): #contructor of the class, which takes two parameters, self refers to the instance of the class and the name parameter which is just a string
        ALModule.__init__(self, name) #calling of the contructpor of the ALModule
        self.tts = ALProxy("ALTextToSpeech", ip, 9559) #proxy creation on the tts module
        self.asr = ALProxy("ALSpeechRecognition", ip, 9559) #proxy creation on the asr module
        self.memory = ALProxy("ALMemory", ip, 9559) #proxy creation on the memory module

        self.num1 = random.randint(1, 10) #here are two integers randomly selected from 1 to 10
        self.num2 = random.randint(1, 10)
        self.operator = random.choice("-") #here is randomly choosen operator which is then applied to the equation
        self.tts.setLanguage("English")  #set the the language which NAO uses for talking

        if self.operator == "-": #NAO was programmed to create equations which have a positive result
            if self.num1 > self.num2: #the numbers are compared in order to asure that the larger number is first
                self.result = str(eval(str(self.num1) + self.operator + str(self.num2))) #the result is evaluated and put into a string so NOA can say it
                self.operator = " minus " #and so is the operator
                self.question = "What is the result of " + str(self.num1) + self.operator + str(self.num2) + "?" #the question is created
            else:
                self.result = str(eval(str(self.num2) + self.operator + str(self.num1)))
                self.operator = " minus "
                self.question = "What is the result of " + str(self.num2) + self.operator + str(self.num1) + "?"
        else:
            self.result = str(eval(str(self.num1) + self.operator + str(self.num2)))
            self.operator = " plus "
            self.question = "What is the result of " + str(self.num1) + self.operator + str(self.num2) + "?"

        print self.question #the question is printed to the terminal
        print self.result #the reslt is printed to the terminal
        self.tts.say(self.question) #NAO tells the question
        self.speech_recognition() #the speech_recognition method is called

    def speech_recognition(self):
        self.asr.setLanguage("English") #this code ensures that NAO will recognize the answer told in English language
        vocabulary = ["zero","one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", \
                     "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
        #vocabylary specifies the words which can be recognize by NAO
        try:
            self.asr.setWordListAsVocabulary(vocabulary) #sets the list of words/phrases (vocabulary) that should be recognized by the speech recognition engine
        except:
            pass #statement does nothing. It can be used when a statement is required syntactically but the program requires no action
        self.memory.subscribeToEvent("WordRecognized", self.getName(), "speech_recognized")
        #subscribes to word recognition and automaticaly launches the getName that declared itself as the generator of the event if required.
        #On recognized is the modules method to call when a data is changed

    def speech_recognized(self, eventName, value, subsIdentifier): #method used by Nao when it receives an answer from the user
        if value[1] > 0.30: #here is the treshold set up
            num = self.get_num(value[0]) #it searches for the word which was said by the user
            num = str(num) #the retrieved value is changed to a string
            print num #it is printed to the terminal
            print value[1] #along with the treshold

            if num == self.result: #the value is  compared and NAO responds to the user acording the answer
                self.tts.say("Your result is correct")
                self.memory.unsubscribeToEvent("WordRecognized", self.getName()) #after subscribing to an event it s neccessary to unsubsribe from it and no more notifications are received
            else:
                self.tts.say("Your result is incorrect the result is " + self.result)
                self.memory.unsubscribeToEvent("WordRecognized", self.getName())
        else:
            print value[1]

    @staticmethod #the following method is a static one, which means that it does not need the initialization of the class
    def get_num(x):
        return { #the method will return number for the given key from this dicionary and it has a default value 0
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "thirteen": 13,
            "fourteen": 14,
            "fifteen": 15,
            "sixteen": 16,
            "seventeen": 17,
            "eighteen": 18,
            "nineteen": 19,
            "twenty": 20,
            }.get(x, 0)