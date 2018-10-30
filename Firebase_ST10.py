import pyrebase
from time import sleep
import datetime
import json
import os
import RPi.GPIO as GPIO
from pi_sht1x import SHT1x

now = datetime.datetime.now()
time1 = now.strftime("%d %B %Y at %H:%M:%S UTC")

#Enter credentials of your firebase real-time database
config = {"apiKey": "Enter your api key here",
          "authDomain": "Enter your auth domain here",
          "databaseURL": "Enter database URL here",
          "projectId": "Enter Project ID",
          "storageBucket": "Enter storage bucket",
          "messagingSenderId": "Enter ms_id"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

userEmail = input("Please Enter Your Email-id \n")
userPass = input("Enter Password \n")

# Log the user in
user = auth.sign_in_with_email_and_password(userEmail, userPass)
print(auth.get_account_info(user['idToken']))

#Creating users
#auth.create_user_with_email_and_password(email, password)

#Verify Email
#auth.send_email_verification(user['idToken'])
#print(auth.get_account_info(user['idToken']))

#Reset Password
#auth.send_password_reset_email(email)

# Get a reference to the database service
db = firebase.database()

while True:
    with SHT1x(18, 23, gpio_mode=GPIO.BCM) as sensor:
        temp = sensor.read_temperature()
        hum = sensor.read_humidity(temp)
        dew1 = sensor.calculate_dew_point(temp, hum)
        
    #data to store        
    data = {'Time Batch': time1, 'Temperature': temp,  'Humidity': hum,  'Dew Point': dew1}
    
    # Pass the user's idToken to the push method
    results = db.child("Pol1").child("Test").push(data, user['idToken'])
    print(str(results) + ", " + str(time1) + ", " + str(temp) + "°C, " + str(hum)+ "%, " + str(dew1) + "°C")
    
    #results = db.child("pol2").child("SHT10").get(user['idToken'])
    sleep(5)
