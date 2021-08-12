from ..databaselayer.testMongoDBConnection import database_setup
from ..businesslogic import classes

def AddNewEvent(db, venue, time, date, duration, eventinfo, eventdetails):
    getDB_details = database_setup(db, "admin")
    getDB_details[2] += 1  #adding another event so sequentially increase ID

    # Make a document to insert in DB
    personDocument = {
        "_id": str(getDB_details[2]),
        "venue": venue,
        "date": date,
        "time": time,
        "duration": duration
    }
    eventdetailsDocument = {
        "_id": str(getDB_details[2]),
        "artist": "-",
        "event_type": "-",
        "available_tickets": "50",
        "specific_requirement": "-"

    }
    # insert in new event specs and also event details in database simultaneouly for the new event
    getDB_details[0].insert_one(personDocument)
    getDB_details[1].insert_one(eventdetailsDocument)

    print("# OF EVENTS IN OUR BACKEND: ")
    print(len(eventinfo))

    #update our variables as well
    tempeventinfo = classes.Event_Specification(getDB_details[2], venue, time, date, duration)
    tempeventdetails = classes.Event_Details(getDB_details[2], "-", "-", "50", "-")
    eventinfo.append(tempeventinfo)
    eventdetails.append(tempeventdetails)

    # print info inserted on terminal
    print("FOLLOWING EVENT INFO HAS BEEN ADDED:")
    print("EVENT ID: " + str(getDB_details[2]))
    print("VENUE:    " + venue)
    print("DATE:     " + date)
    print("TIME:     " + time)
    print("DURATION: " + duration)
    
    return True


def SellTickets(db, evid, typeofticket, seat_num, eventdetails, ticketslist):

    for each in eventdetails:
        each.event_print()
    print()
    for each in ticketslist:
        for t in ticketslist[each]:
            t.ticket_print()
    print()

    getDB_details = database_setup(db, "fdo")
    getDB_details[1] += 1   #Adding another ticket so sequentially increase ID
    totaltickets = 0 

    breakornot = True                   #check to see if event exists if event does not exist can not sell tickets
    for each in eventdetails:
        if each.event_id == evid:
            totaltickets = each.total_tickets       #if event does exist need to check if any more tickets can be sold or not
            breakornot = False
            break

    if breakornot:                     #if event does not exist return false without any further work
        return False

    print("TOTAL TICKETS")
    print(int(totaltickets))

    #if this is the first ticket of the event make a list of it in our dict
    if evid not in ticketslist:
        ticketslist[evid] = list()

    if len(ticketslist[evid]) < int(totaltickets):  #check if the number of sold tickets is equal to total tickets for event only continue further if tickets are available
        # Make a document to insert in DB
        ticketDocument = {
            "_id": str(getDB_details[1]),
            "event_id": evid,
            "typeofticket": typeofticket,
            "seat_num": seat_num
        }

        #insert in database
        getDB_details[0].insert_one(ticketDocument)

        # print info inserted on terminal
        print("FOLLOWING TICKET INFO HAS BEEN ADDED:")
        print("TICKET ID: " + str(getDB_details[1]))
        print("EVENT ID:    " + evid)
        print("TICKET TYPE:    " + typeofticket)
        print("SEAT NUMBER:    " + seat_num)

        #update our variables as well
        tempticket = classes.Ticket(getDB_details[1],evid,typeofticket,seat_num)
        ticketslist[evid].append(tempticket)

        return True

    else:
        return False


def CancelTicket(db, tid, tickets):
    getDB_details = database_setup(db, "fdo")
    ticketDocument = getDB_details[0].find_one({"_id": tid})

    if ticketDocument != None:
        print("FOLLOWING TICKET INFO HAS BEEN DELETED:")
        print("TICKET ID: " + ticketDocument["_id"])
        print("EVENT ID:    " + ticketDocument["event_id"])
        print("TICKET TYPE:    " + ticketDocument["typeofticket"])
        print("SEAT NUMBER:    " + ticketDocument["seat_num"])
        getDB_details[0].delete_one({"_id": tid})

        #update our own variables    
        breakornot = False
        for key in tickets:
            for each in tickets[key]:
                if each.ticket_id == tid:
                    tickets[key].remove(each)
                    breakornot = True
                    break
            if breakornot:
                break

        return True
    else:
        return False


def DeleteEvent(db, evid, eventsinfo, eventdetails, tickets):
    getDB_details = database_setup(db, "admin")
    eventDocument = getDB_details[0].find_one({"_id": evid})
    eventDocument2 = getDB_details[1].find_one({"_id": evid})

    if eventDocument != None and eventDocument2 != None:
        # print info of deleted event on terminal
        print("FOLLOWING EVENT INFO HAS BEEN DELETED:")
        print("EVENT ID: " + eventDocument["_id"])
        print("VENUE:    " + eventDocument["venue"])
        print("DATE:     " + eventDocument["date"])
        print("TIME:     " + eventDocument["time"])
        print("DURATION: " + eventDocument["duration"])

        # print info of deleted event on terminal
        print("FOLLOWING EVENT INFO HAS BEEN DELETED:")
        print("EVENT ID: " + eventDocument2["_id"])
        print("ARTIST:    " + eventDocument2["artist"])
        print("EVENT TYPE:     " + eventDocument2["event_type"])
        print("AVAILABLE TICKETS:     " + eventDocument2["available_tickets"])
        print("SPECIFIC REQUIREMENT: " + eventDocument2["specific_requirement"])

        # deleting all tickets associated with the event being deleted
        getTicketDB = database_setup(db, "fdo")
        getTicketDB[0].delete_many({"event_id": evid})

        # delete both event specifications and event details
        getDB_details[0].delete_one({"_id": evid})
        getDB_details[1].delete_one({"_id": evid})

        #update our current variables in backend as well
        for each in eventdetails:
            if each.event_id == evid:
                eventdetails.remove(each)
                break
        for each in eventsinfo:
            if each.event_id == evid:
                eventsinfo.remove(each)
                break
        for key in tickets:
            if key == evid:
                tickets.pop(key)
                break

        return True

    else:
        return False


def EditEventInfo(db, evid, ven, t, dt, dur, eventinfo):
    getDB_details = database_setup(db, "admin")
    personDocument = getDB_details[0].find_one({"_id": evid})
    if personDocument != None:
        getDB_details[0].update_one({"_id":evid}, {"$set": {"venue": ven, "date":dt, "time":t, "duration":dur}}, upsert=False)
        
        #update our own variables as well 
        for each in eventinfo:
            if each.event_id == evid:
                each.UpdateEventSpecs(ven,t,dt,dur)
                break
        
        return True
    else:
        return False

        
def EditEventDetails(db, evid, artist, eventtype, totaltickets, req, eventdetails):
    getDB_details = database_setup(db, "admin")
    eventdetailsDocument = getDB_details[1].find_one({"_id": evid})
    if eventdetailsDocument != None:
        getDB_details[1].update_one({"_id": evid}, {"$set" : {"artist" : artist, "event_type":eventtype, "available_tickets": totaltickets, "specific_requirement": req}}, upsert= False)
        
        #update our own variables as well 
        for each in eventdetails:
            if each.event_id == evid:
                each.UpdateEventDetails(artist,eventtype,totaltickets,req)
                break
        
        return True
    else:
        return False

def EditTicket(db, tid, seat_num, typeofticket, ticketlist):
    getDB_details = database_setup(db, "fdo")
    ticketDocument = getDB_details[0].find_one({"_id": tid})
    if ticketDocument != None:
        getDB_details[0].update_one({"_id": tid}, {"$set" : {"typeofticket": typeofticket, "seat_num": seat_num}},upsert=False)
        
        #update our own variables as well 
        for each in ticketlist:
            if each.ticket_id == tid:
                each.UpdateTicket(seat_num, typeofticket)
                break
        
        return True
    else:
        return False

def ViewEventCatalogue(events_info, event_details, evid):
    tosend = list()
    if evid != 'all' and evid != '-' and evid != 'ALL':    
        for each in event_details:
            if each.event_id == evid:
                store1 = classes.Event_Details(each.event_id, each.artist, each.event_type, each.total_tickets, each.specific_requirement)
                break
        for each in events_info:
            if each.event_id == evid:
                store2 = classes.Event_Specification(each.event_id,each.venue, each.time, each.date, each.duration)
                break
        tosend.append( "EVENT INFORMATION:")
        temp = classes.Display(store1, store2)
        for each in temp:
            tosend.append(each)
        tosend.append("=========================================")
    else:
        tosend = list()
        tosend.append( "EVENT INFORMATION:")
        i = 0
        while i < len(events_info):
            store1 = classes.Event_Details(event_details[i].event_id, event_details[i].artist,event_details[i].event_type, event_details[i].total_tickets, event_details[i].specific_requirement)
            store2 = classes.Event_Specification(events_info[i].event_id,events_info[i].venue, events_info[i].time, events_info[i].date, events_info[i].duration)
            temp = classes.Display(store1, store2)
            for each in temp:
                tosend.append(each)
            tosend.append("=========================================")
            i += 1
    return tosend