import RPi.GPIO as GPIO
import time

def alarm():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(37, GPIO.OUT)
	GPIO.output(37, GPIO.HIGH)
	time.sleep(4)
	GPIO.output(37, GPIO.LOW)
	GPIO.cleanup()
