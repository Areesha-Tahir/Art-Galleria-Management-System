
import pymongo
from pymongo import MongoClient
import django
from ..businesslogic import classes
    
def database_connection():
    #SETTING UP DATABASE
    #client = MongoClient("mongodb+srv://<username>:<password>@cluster0.nhmcd.mongodb.net/SE?retryWrites=true&w=majority")
    #Here instead of <username> write your mongoDB atlas username and instead of <password> write the corresponding password for your account
    db = client["SE"]

    client.close()
    return db
    
def setUpData(eventinfo, eventdetails, tickets, db):
    event_specs = db["Event_Specifiction"]
    event_details=db["Event_Details"]
    tickets_db = db["Tickets"]
    event_count = event_specs.count()
    ticket_count = tickets_db.count()
    
    #get data from database and store in our list 
    getresults1 = event_specs.find()
    getresults2 = event_details.find()
    i = 0 
    while i < event_count:
        id = getresults1[i]["_id"]
        v = getresults1[i]["venue"]
        dt = getresults1[i]["date"]
        t = getresults1[i]["time"]
        dur = getresults1[i]["duration"]
        art = getresults2[i]["artist"]
        ty = getresults2[i]["event_type"]
        av_tckts = getresults2[i]["available_tickets"]
        req = getresults2[i]["specific_requirement"]

        tempeventinfo = classes.Event_Specification(id, v, t, dt, dur)
        tempeventdetails = classes.Event_Details(id, art, ty, av_tckts, req)
        eventinfo.append(tempeventinfo)
        eventdetails.append(tempeventdetails)
        i+=1

    getresults = tickets_db.find()
    i = 0
    while i < ticket_count:
        t_id = getresults[i]["_id"]
        ev_id = getresults[i]["event_id"]
        st = getresults[i]["seat_num"]
        ty = getresults[i]["typeofticket"]
        tempticket = classes.Ticket(t_id, ev_id, st, ty)
        if ev_id not in tickets:
            tickets[ev_id] = list()
            tickets[ev_id].append(tempticket)
        else:
            tickets[ev_id].append(tempticket)
        i+=1

def database_setup(db, condition):

    #get each collection and their count for auto ID generation
    event_specs = db["Event_Specifiction"]
    event_details=db["Event_Details"]
    getresults = event_specs.find() #get all the documents in a mongoDB Cursor (kind of like an array)
    event_count = event_specs.count() #get count of total documents stored in collection currently 
    print("EVENT COUNT: ", end = "")
    print(event_count)
    if (event_count > 0):
        event_count = int(getresults[event_count-1]["_id"]) #get the ID of the last document (IDs will always be in chronologically increasing order so last will be current highest)
    elif (event_count == 0):
        event_count = -1

    tickets=db["Tickets"]
    getresults = tickets.find()
    tickets_count=tickets.count()
    print("TICKET COUNT: ", end = "")
    print(tickets_count)
    if(tickets_count > 0):
        tickets_count = int(getresults[tickets_count-1]["_id"])
    elif(tickets_count == 0):
        tickets_count = -1

    toReturn = list()

    if(condition == "admin"):
        toReturn.append(event_specs)
        toReturn.append(event_details)
        toReturn.append(event_count)
        return toReturn

    if(condition == "fdo"):
        toReturn.append(tickets)
        toReturn.append(tickets_count)
        toReturn.append(event_specs)
        return toReturn
