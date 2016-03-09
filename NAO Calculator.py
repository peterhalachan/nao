#NAO Calculator
from Tkinter import * #from the Tkinter module is everything imported
from naoqi import ALProxy #from naoqi module ALProxy is imported

# ip variable
ip = "192.168.0.106" #ip address od robot
port = 9559 #port number

tts = ALProxy("ALTextToSpeech", ip, port) #proxy creation on the tts module
tts.setParameter("pitchShift", 1.0) #sets the pitch shift of Nao's voice
tts.setVolume(1.0) # sets the volume of speech


def frame(root, side): #this is a method used for placing buttons into a frame
    frame = Frame(root) #Frame is a widget used for grouping and organizing other widgets in a somehow friendly way. It works like a container, which is responsible for arranging the position of other widgets.
    frame.pack(side=side, expand=YES, fill=BOTH) #pack is  geometry manager which organizes widgets in blocks before placing them in the parent widget.
    #Side determines which side of the parent widget packs against
    #When expand is set to true, widget expands to fill any space not otherwise used in widget's parent.
    #Fill is used for filling space in X or Y or both directions
    return frame #returns a frame widget


def button(root, side, text, command=None): #method used for creating buttons
    frame = Button(root, text=text, command=command) #The Button widget is used to add buttons in a Python application. These buttons can display text or images that convey the purpose of the buttons. You can attach a function or a method to a button which is called automatically when you click the button.
    frame.pack(side=side, expand=YES, fill=BOTH) #The same as in frame method
    return frame #returns a button widget


class Calculator(Frame): #this class inherits from the Frame container widget
    def __init__(self): #contructor of the Calculator Class. It has a self attribute refering to the instance of the class
        Frame.__init__(self) #calling of the Frame contructor
        self.pack(expand=YES, fill=BOTH)
        self.master.title('NAO Calculator') #Adds a tiitle to the interface

        display = StringVar() #display is a container for a string value used for displaying the equations and results on the interface
        entry = Entry(self, relief=SUNKEN, textvariable=display, state=DISABLED).pack(side=TOP, expand=YES, fill=BOTH) #The Entry widget is used for displaying multiple lines of text
        #relief=SUNKEN creates a feeling that the entry is like "sunk in"
        #textvariable=display displays the equations and results
        #state=DISABLED causes that the user will not type into the entry
        #the pack method specifies where it will be placed

        for keyboard_row in ("123", "456", "789", "-0."): #this loop will iterate through each row of the calculator
            key_frame = frame(self, TOP) #for each key is created a frame
            for key in keyboard_row: #this iterates through each key in a row
                button(key_frame, LEFT, key, lambda frame=display, c=key: frame.set(frame.get()+c)) #calling of the button function, it will be placed into a frame called key_frame, to left side, key stores the character which is displayed on the button and at the is the function defined of the key

        operator_frame = frame(self, TOP)  #calling of frame function for the creation of a frame for operator buttons
        for operator in "+*/=": #this loop iterates through the operators of the calculator
            if operator == '=': #for the equal sign there is a different procedure compared to other operators
                btn = button(operator_frame, LEFT, operator) #it takes only 3 parameters: frame, placed to the left side and the char which is the equal sign
                btn.bind('<ButtonRelease-1>', lambda e, s=self, frame=display: s.calc(frame)) #bind method is used for adding a functinality to the button. The left mouse button will execute the button functionality, which is the evaluation of the equation

            else:
                btn = button(operator_frame, LEFT, operator, lambda frame=display, s=operator: frame.set(frame.get()+s))

        clear_frame = frame(self, BOTTOM) #frame for the C button, which is used for erasing the entry
        button(clear_frame, LEFT, 'C', lambda frame=display: frame.set(''))

    def calc(self, display): #method used for evaluation of the displayed equation
        try: #this is used for handling exceptions. These commands occur if the showed equation can be evaluated
            equation = str(display.get()) #the equation will be translated to a string and stored in the variable
            result = str(eval(display.get())) #the same goes for the result
            display.set(eval(display.get())) #displays the result on the interface
            print("The result of %s is %s") % (equation, result) # the equation and the result is printed to the terminal

            sentence = "" #declaration of the variable used by NAO to say the operator properly
            for char in equation: #iterates through the equation to find all the operators stores it into the sencet
                if char == "+":
                    sentence += " plus "
                elif char == "*":
                    sentence += " multiplied by "
                elif char == "/":
                    sentence += " divided by "
                elif char == "-":
                    sentence +=" minus "
                else:
                    sentence += char # if the character is not a operator it is is not changed and just stored into the sentece
            tts.say("The result of " + sentence + " is " + result) #Nao says the equantion and the result
        except:
            display.set("Error") #in case it can not evaluate the equation it prints on the interface "Error"

Calculator().mainloop() #the class is iterated in an infinite loop so the user able to use it