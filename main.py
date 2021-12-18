from datetime import datetime
# from flask import Flask, request
# import telegram
import requests
import os
import schedule
import time
# import json
import pytz
from replit import db
import keep_alive

# token = os.environ.get('token')
token = os.environ['token']
base_url = "https://api.telegram.org/bot"
help_msg = "'optin' to recieve birthday notifications \n'optout' to stop receiving birthday notifications \n'thismonth' to get the names of all people who have birthday this month\n'hi' to say hi to the bot"


parameters = {
    "offset":"236946795",
    "limit":1
}
del db["month"]
db["month"] = {"1":{"10":"Dhatri", "19":"Arun"},
"2":{},
"3":{"22":"Manikanta" , "20":"Omkaradithya" ,"24":"Vishwanath", "3":"Vaishnavi"},
"4":{"15":"Amulya" , "29":"Chirag" , "18":"Srikaran" },
"5":{"12":"Digjoy" , "30":"Datta" , "5":"Vojeswitha"},
"6":{},
"7":{"20":"Adarsh" },
"8":{"12":"Pranav", "15":"Abhiroop" , "9":"Vijay" , "25":"Tanmay"   },
"9":{"10":"Varshitha" , "24":"Sachi and Adhvik"},
"10":{"14":"Sujal" , "25":"Vaibhav" },
"11":{"7":"Yashas"},
"12":{"14":"Haritha" ,"19":"Just for testing" , "22":"Dishank" , "31":"Nwjwr" ,"28":"Tanay" }
}

# print(str(db["month"]["12"]))
# print(datetime.now())

def day_and_month():
  tz_IN = pytz.timezone("Asia/Kolkata")
  day = datetime.now(tz_IN).date().day
  month = datetime.now(tz_IN).date().month
  return day , month

def sendmsg(chatId, text):
    requests.get(base_url+token+"/sendMessage", data={"chat_id":chatId,"text":text})

def sendNow():
    tz_IN = pytz.timezone('Asia/Kolkata')
    day = datetime.now(tz_IN).date().day
    month = datetime.now(tz_IN).date().month

    if str(day) in db["month"][str(month)]:
      name = db["month"][str(month)][str(day)]
      
    # print(specialNum)
    # print("yes\n\n\n\n")
    # if specialNum == 0:
      for chatId in db["sendingList"]:
        requests.get(base_url+token+"/sendMessage", data = {"chat_id":chatId, "text":"Today is the birthday of "+name}) 



def getUpdates():
    resp = requests.get(base_url+token+"/getUpdates",data=parameters)
    # print(resp.text)
    # with open("newfile.json","w+") as f:
        # json.dump(resp.json(), f)
    # print(resp.text)
    resp = resp.json()
    if not resp["result"]:
      # print("no")
      return
    if "message" not in  resp["result"][0] and "edited_message" not in resp["result"][0]:
        # print("yes")
        parameters["offset"] = str(int(resp["result"][-1]["update_id"])+1)
        return
    # print(resp.text)
    msg = ["message","edited_message"]
    flag = 0
    if "message" not in resp["result"][0]:
      flag = 1

    chatId = resp["result"][0][msg[flag]]["chat"]["id"]
    if resp["result"][0][msg[flag]]["text"].lower() == "optin":
        if chatId not in db["sendingList"]:
            db["sendingList"].append(chatId)
            sendmsg(chatId,"You have opted in to recieve notifications about birthdays, send 'optout' to opt out")
        else:
            sendmsg(chatId,"You are already signed up to recieve notifications about birthdays, send 'optout' to opt out")

    if resp["result"][0][msg[flag]]["text"].lower() == "optout":
         if chatId in db["sendingList"]:
            db["sendingList"].remove(chatId)
            sendmsg(chatId,"You have opted out, send 'optin' to opt in again")

    if resp["result"][0][msg[flag]]["text"].lower() == "thismonth":
      sendmsg(chatId , str(db["month"][str(day_and_month()[-1])]))
    
    if resp["result"][0][msg[flag]]["text"].lower() == "/help":
      sendmsg(chatId , help_msg )
    if resp["result"][0][msg[flag]]["text"].lower() == "hi":
      sendmsg(chatId , "hello! "+resp["result"][0][msg[flag]]["from"]["first_name"] )
    parameters["offset"] = str(int(resp["result"][-1]["update_id"])+1)
    # print(parameters["offset"])
    # print(db["sendingList"])

# def spam():
#     resp = requests.get(base_url+token+"/getUpdates",data=parameters)
#     print(resp.text)
# spam()

keep_alive.keep_alive()    

schedule.every(1).day.at("01:00").do(sendNow)

while True:
    getUpdates()
    schedule.run_pending()
    time.sleep(0.5)
    # print(db["sendingList"])

# def work():
#     resq = requests.get(base_url+token+"/getUpdates?offset=0")
#     print(resq.text)
# work()
