from datetime import datetime
from flask import Flask, request
import telegram
import requests
import os
import schedule
import time
import json
import pytz
token = os.environ.get('token')

base_url = "https://api.telegram.org/bot"

parameters = {
    "offset":"236946711"
    # "limit":"1"    
}

sendingList = []
def sendmsg(chatId, text):
    requests.get(base_url+token+"/sendMessage", data={"chat_id":chatId,"text":text})

def sendNow():
    tz_IN = pytz.timezone('Asia/Kolkata')
    day = datetime.now(tz_IN).date().day
    month = datetime.now(tz_IN).date().month
    specialNum = datetime.now(tz_IN).time().minute % 2
    # print(specialNum)
    # print("yes\n\n\n\n")
    if specialNum == 0:
        for chatId in sendingList:
            requests.get(base_url+token+"/sendMessage", data = {"chat_id":chatId, "text":"its working"}) 

def getUpdates():
    resp = requests.get(base_url+token+"/getUpdates",data=parameters)
    print(resp.text)
    # with open("newfile.json","w+") as f:
        # json.dump(resp.json(), f)
    resp = resp.json()
    if not resp["result"]:
        return
    chatId = resp["result"][0]["message"]["chat"]["id"]
    if resp["result"][0]["message"]["text"].lower() == "optin":
        if chatId not in sendingList:
            sendingList.append(chatId)
            sendmsg(chatId,"You have opted in to recieve notifications about birthdays, send 'optout' to opt out")
        else:
            sendmsg(chatId,"You are already signed up to recieve notifications about birthdays, send 'optout' to opt out")

    if resp["result"][0]["message"]["text"].lower() == "optout":
         if chatId in sendingList:
            sendingList.remove(chatId)
            sendmsg(chatId,"You have opted out, send 'optin' to opt in again")

    parameters["offset"] = str(int(resp["result"][-1]["update_id"])+1)
    print(parameters["offset"])
    print(sendingList)

# def spam():
#     resp = requests.get(base_url+token+"/getUpdates",data=parameters)
#     print(resp.text)
# spam()
    
schedule.every(1).minute.do(sendNow)

while True:
    getUpdates()
    schedule.run_pending()
    time.sleep(10)

# def work():
#     resq = requests.get(base_url+token+"/getUpdates?offset=0")
#     print(resq.text)
# work()