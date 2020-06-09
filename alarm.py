#!/usr/bin/ python2
# -*- coding: utf8 -*-


import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import smtplib

mailSent=False

def mailer():
	global mailSent
	if mailSent==False:
		server=smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login("generic@gmail.com", "generic")
		server.mail("generic@gmail.com")
		server.rcpt("Number@vtext.com")
		server.data("Subject: Alarm\nYour alarm has been triggered")
		server.quit()
		mailSent=True


GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,  GPIO.IN)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)


alarmed=False
detected=False
start=0
downCount=0
count=0
counts=True
counting=True
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


#turn on and off led's
def led(g, r):
	if g==0:
		GPIO.output(38,GPIO.LOW)
	if g==1:
		GPIO.output(38, GPIO.HIGH)
	if r==0:
		GPIO.output(36, GPIO.LOW)
	if r==1:
		GPIO.output(36, GPIO.HIGH)

def buzzer(b):
	if (b==0):
		GPIO.output(32, GPIO.LOW)
	if (b==1):
		GPIO.output(32, GPIO.HIGH)


#create an unarm/arm function
def armed():
	global alarmed
	global count
	global counts
	global detected
        detected=False
	print "Matching card detected"
	countdownStart=time.time()
	if alarmed==True:
		alarmed=False
		led(1, 0)
		buzzer(0)
		count=0
		print "disarmed"
		mailSent=False
	else:
		mailSent=False
		counts=True
		led(0, 1)
		buzzer(0)
		count=0
		while counts:
			counter=time.time()-countdownStart
			counter=int(counter)
			print counter
			if counter%2==0:
				led(0, 1)
			else:
				led(0,0)
			if counter>90:
				led(0,1)
				alarmed=True
				counts=False
				print "Arming"
				mailSent=False

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Martin's Home Alarm"
led(1, 0)
buzzer(0)
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    if alarmed==True and counts==False:
    	motion=GPIO.input(40)
    	if motion==1 and mailSent==False and detected==False:
		count=count+1
		detected=True
		print "Motion detected"
	if count==1:
		start=time.time()
		print "start at 1"
		count=count+1
	if count>=2:
		print count
		count=count+1
		downCount=time.time()-start
		print downCount
		if count%2==0:
			led(0,0)
			buzzer(0)
		else:
			led(0,1)
			buzzer(1)
		if downCount>40:
			led(0,1)
			count=0
			print "Sounding alarm"
			mailer()
				


    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status==MIFAREReader.MI_OK:
        print "card"
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status==MIFAREReader.MI_OK:
        print "work"
        # Print UID and check if it matches
        print "Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
        
	if uid[0]==86 and uid[1]==149 and uid[2]==235 and uid[3]==52 or uid[0]==97 and uid[1]==216 and uid[2]==20 and uid[3]==137:
			armed()
			mailSent=False
                       #wait half a second to do anything. Helps prevent double reads
    
        

