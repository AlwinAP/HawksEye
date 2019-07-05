"""
@Project: Hawks Eye - Motion detector
@Author: Alwin Prabu
@Filename: motion-detector.py
"""
# Python libraries to be imported 
import time
import datetime
import smtplib 
import RPi.GPIO as GPIO
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

#Configuration
storeNumber = 17  # Change it for each store room device
fromaddr = "device@clientsite.com"  # Change it as per client requirements
toaddr = "security@watfordss.com"   # Change it as per client requirements

# Main program
sensor = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

while True:
    time.sleep(0.1)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    if current_state != previous_state:
	  # Motion detected
        new_state = "HIGH" if current_state else "LOW"
		print("GPIO pin %s is %s" % (sensor, new_state))
		
	  # instance of MIMEMultipart 
        msg = MIMEMultipart() 
        
        # storing the senders email address 
        msg['From'] = fromaddr 
        
        # storing the receivers email address 
        msg['To'] = toaddr 
		
        # storing the subject 
        msg['Subject'] = "Motion Detected by Hawk’s Eye in Store Room No:" + storeNumber
        
        # string to store the body of the mail 
        body = "Alarm triggered on " + datetime.datetime.now() + " at " + datetime.datetime.now().time()
        
        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 
        
        # open the file to be sent 
        filename = "File_name_with_extension"
        attachment = open("/home/pi/capture.png", "rb") 
        
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
        
        # encode into base64 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 

        # creates SMTP session 
        server = smtplib.SMTP('smtp.gmail.com', 587) 
		
	      # start TLS for security 
        server.starttls()
		
        # Authentication
        server.login(fromaddr, "Password_of_the_sender")
		
	      # Converts the Multipart msg into a string 
        text = msg.as_string() 
		
        # sending the mail 
        server.sendmail(fromaddr, toaddr, text) 
		
	      # terminating the session 
        server.quit()
