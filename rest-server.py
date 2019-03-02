#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
from requests.utils import quote
from twilio.rest import Client
from collections import defaultdict
import schedule
import time
#import MySQLdb
import pymysql
import sys
import csv
import requests 
import json
import scraper
app = Flask(__name__, static_url_path="")


USERNAME = 'tapas'
PASSWORD = 'password'
DB_NAME = 'opendata'
# ##
# # Insert host url from RDS
# connect = MySQLdb.connect (	host = "",
#                          	user = USERNAME,
#                          	passwd = PASSWORD,
#                          	db = DB_NAME, 
#  				            port = 3306)

# conn  = connect.cursor()

con = pymysql.connect(host="", user=USERNAME, password=PASSWORD, db=DB_NAME, cursorclass=pymysql.cursors.
                                   DictCursor)
cur = con.cursor()

@app.route('/', methods=['GET'])
def getHome():
    return render_template('index.html')

@app.route('/updateEvents')
def getEvents():
    with open('events.json') as f:
        f.write(scraper.Events().json)

@app.route('/miguel')
def miguel():
    return 'Miguel Called this route'

@app.route('/tapas')
def tapas():
    cur.execute("SELECT phonenumber, fname FROM contactpeeps LIMIT 50")
    result = cur.fetchall()
    print(result)
    return "result"

@app.route('/kyle')
def kyle():
    numbers_dict = defaultdict(lambda: "")
    numbers_dict["14048191425"] = "Tapas Kapadia"
    message_string = "you suck ill eat ur pea brain"
    notify_events(numbers_dict, message_string)
    return 'sent'


# numbers_dict = defaultdict(lambda: "")
# numbers_dict["+17176391921"] = "Dalton"
# numbers_dict["+15183547556"] = "Kyle"
# numbers_dict["+17138359559"] = "Pea Brain"
# numbers_dict["+17138359559"] = "Tapas Kapadia"
# message_string = "you suck ill eat ur pea brain"

# (list, string)
def notify_events(numbers, message):
    for number, name in numbers.items():
        
        # Twilio Authentication
        account_sid = "ACd1710704a119c7266c11e227a40408fb" 
        auth_token = "c1a7bde509f696defe6c8836eabee114"
        sms_string = "Hi " + name + "!!!, " + message
        
        client = Client(account_sid, auth_token)
        media_url = "https://tse1.mm.bing.net/th?id=OIP.cV7nTqlOSi88l2-5o_IdewHaIy&pid=Api"
        response = client.messages.create(
            to= number, 
            from_= "+17176198944",
            body= sms_string,
            media_url= media_url # if you need to attach multimedia to your message, else remove this parameter.
        )
        print(response.sid)
        
#notify_events(numbers_dict, message_string)
        
'''    
schedule.every().day.at("08:00").do(notify_events)
   
while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
'''



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=3001)
    
