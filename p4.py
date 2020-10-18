

# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time
import sys
# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
count=0
led_pwm=0
# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()
guess_value=0
value=0
score_counter=0
num_ofGuesses=0
# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")

# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":   
	
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        global value
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    pass

#callback funbctions
def callback_increase(channel):
    print("btn_increased callback")
    btn_increase_pressed()
    pass
def callback_submit(channel):
    print("btn_submit")
    btn_guess_pressed()
    pass
# Setup Pins
def setup():
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Setup regular GPIO
    GPIO.setup(btn_submit,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_increase,GPIO.IN,pull_up_down=GPIO.PUD_UP)  #button setup

    GPIO.setup(LED_value[0],GPIO.OUT)  #led1 setup
    GPIO.setup(LED_value[1],GPIO.OUT) #led2 setup
    GPIO.setup(LED_value[2],GPIO.OUT) #led3 setup
    GPIO.setup(LED_accuracy,GPIO.OUT) #accuracy led setup
  #  GPIO.output(buzzer,GPIO.OUT)  #buzzer setup

    #set leds to low initially
    GPIO.output(LED_value[0],GPIO.LOW)
    GPIO.output(LED_value[1],GPIO.LOW)
    GPIO.output(LED_value[2],GPIO.LOW)
   # GPIO.output(buzzer,GPIO.LOW)
    # Setup PWM channel
    global led_pwm 
    led_pwm=GPIO.PWM(LED_accuracy,500)
 #   buzzer_pwm=GPIO.PWM(buzzer,1000)
    
    led_pwm.start(0)
    # Setup debouncing and callbacks
    GPIO.add_event_detect(btn_increase,GPIO.FALLING,callback=callback_increase,bouncetime=500) #event listener with call back that fires the btn_increase_pressed function
    GPIO.add_event_detect(btn_submit,GPIO.BOTH,callback=callback_submit,bouncetime=500)  #event listener with callback that fires btn_submit method
    pass

def count_fix(counter):
	global count
	counter=count
	if count==8:
		count=0
# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = eeprom.read_byte(0)
    # Get the scores
    
    # convert the codes back to ascii
    
    # return back the results
    return score_count, scores


# Save high scores
def save_scores(name,guess):
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores	
   
    for i in name:
    	#eeprom.write
    	pass
    print("Hey "+name + "you won just after "+ str(guess)+" guesses")
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3))


# Increase button pressed
def btn_increase_pressed():
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a gues 
	print("btn_increase_pressed")
	global guess
	global count
	count=count+1
	counter=count
	count_fix(counter)
	if counter==0:
		GPIO.output(LED_value[0],False)
		GPIO.output(LED_value[1],False)
		GPIO.output(LED_value[2],False)
		print(counter)
		print(count)
	elif counter==1:
		GPIO.output(LED_value[0],True)
		GPIO.output(LED_value[1],False)
		GPIO.output(LED_value[2],False)
		print(counter)
		print(count)
	elif counter==2:
		GPIO.output(LED_value[0],False)
		GPIO.output(LED_value[1],True)
		GPIO.output(LED_value[2],False)
	elif counter==3:
		GPIO.output(LED_value[0],True)
		GPIO.output(LED_value[1],True)
		GPIO.output(LED_value[2],False)
		print(counter)
	elif counter==4:
		GPIO.output(LED_value[0],False)
		GPIO.output(LED_value[1],False)
		GPIO.output(LED_value[2],True)
		print(counter)
	elif counter==5:
		GPIO.output(LED_value[0],True)
		GPIO.output(LED_value[1],False)
		GPIO.output(LED_value[2],True)
		print(counter)
	elif counter==6:
		GPIO.output(LED_value[0],False)
		GPIO.output(LED_value[1],True)
		GPIO.output(LED_value[2],True)
		print(counter)
	elif counter==7:
		GPIO.output(LED_value[0],True)
		GPIO.output(LED_value[1],True)
		GPIO.output(LED_value[2],True)
	pass


# Guess button
def btn_guess_pressed():
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
   # GPIO.output(LED_value[1],GPIO.HIGH)
	global score_counter
	global count
	global value
	global num_ofGuesses
	num_ofGuesses=num_ofGuesses+1
	global guess_value
	guess_value=count
	diff=guess_value-value
#    accuracy_leds(guess_value,value)
	if abs(diff)==0:
    	#win the game 
		GPIO.output(LED_value,GPIO.LOW)
		GPIO.output(LED_accuracy,GPIO.LOW)
    	#GPIO.output(buzzer,GPIO.HIGH)
		score_counter=score_counter+1
		eeprom.write_byte(0,score_counter)
		print("you won the game!!!\n")
		print("You won after "+str(num_ofGuesses) + " guesses")
		name=input("Enter your 3  letter long name: ")
		while len(name) !=3:
			name=input("Try again with a 3 letter long name: ")
		save_scores(name,num_ofGuesses)
		num_ofGuesses=0
		menu()

	pass


# LED Brightness
def accuracy_leds(guessed_val,answer):
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    global dc
    
    if guessed_val<answer:
    	dc=(guessed_val/answer)*100
    	led_pwm.ChangeDutyCycle(dc)
    else:
    	dc=((8-guessed_val)/(8-answer))*100
    	led_pwm.ChangeDutyCycle(dc)
    
    pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
