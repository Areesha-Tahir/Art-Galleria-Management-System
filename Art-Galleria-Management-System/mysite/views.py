from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.shortcuts import render
from .forms import EditEventDetailsForm, EditTicketsForm, LoginForm, EditEventInfoForm, ViewEventsForm, ViewTicketsForm
from .forms import AddEvent
from .forms import CancelTicket
from .forms import SellTickets
from .forms import DeleteEvent
from .businesslogic.businesslogic_main import AddNewEvent as b_AddEvent
from .businesslogic.businesslogic_main import SellTickets as b_SellTickets
from .businesslogic.businesslogic_main import CancelTicket as b_CancelTicket
from .businesslogic.businesslogic_main import DeleteEvent as b_DeleteEvent
from .businesslogic.businesslogic_main import EditTicket as b_EditTicket
from .businesslogic.businesslogic_main import EditEventDetails as b_EditEventDetails
from .businesslogic.businesslogic_main import EditEventInfo as b_EditEventInfo
from .businesslogic.businesslogic_main import ViewEventCatalogue as b_ViewEventCatalogue
from .databaselayer.testMongoDBConnection import database_connection
from .databaselayer.testMongoDBConnection import setUpData
from .businesslogic import classes


"""=====================================================================================================
                                        SET UP DATA/VARIABLES IN START
========================================================================================================"""
#set up a database connection only once
db = database_connection() 
events_info = list()            #list of all events information
event_details = list()          #list of all events details
tickets = dict()                #list of each event's available tickets

setUpData(events_info, event_details, tickets, db)

for each in events_info:
    each.event_print()
print()
for each in event_details:
    each.event_print()
print()
for each in tickets:
    for t in tickets[each]:
        t.ticket_print()
print()

print("SUCCESSFUL END")

"""=====================================================================================================
                                    CONTROLLER FUNCTIONS
========================================================================================================"""
def homeadmin(request):
    template = loader.get_template("homeadmin.html")
    # passing dictionary will help us inject data to our webpage
    return HttpResponse(template.render({}, request))


def homefdo(request):
    template = loader.get_template("homefdo.html")
    # passing dictionary will help us inject data to our webpage
    return HttpResponse(template.render({}, request))

def login(request):
    if(request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            actor = form.cleaned_data["Name"]
            if(actor == "Admin"):
                return render(request, "homeadmin.html", {"form": form})
            elif(actor == "FDO"):
                return render(request, "homefdo.html", {"form": form})
    else:
        form = LoginForm()
    template = loader.get_template("accounts/login.html")
    # passing dictionary will help us inject data to our webpage
    return HttpResponse(template.render({"form": form}, request))


def AddNewEvent(request):
    if(request.method == "POST"):
        form = AddEvent(request.POST)
        if(form.is_valid()):
            ven = form.cleaned_data["venue"]
            t = form.cleaned_data["time"]
            dt = form.cleaned_data["date"]
            dur = form.cleaned_data["duration"]
            if b_AddEvent(db, ven, t, dt, dur, events_info, event_details):
                messages.success(request, "EVENT ADDED SUCCESSFULLY!")
            else:
                messages.error(request, "ERROR: EVENT NOT ADDED")
    else:
        form = AddEvent()
    return render(request, "AddEvent.html", {"form": form})


def Delete_Event(request):
    if(request.method == "POST"):
        form = DeleteEvent(request.POST)
        if(form.is_valid()):
            eventid = form.cleaned_data["eventid"]
            if b_DeleteEvent(db, eventid, events_info, event_details, tickets):
                messages.success(request, "EVENT SUCCESSFULLY DELETED")
            else:
                messages.error(request, "ERROR: EVENT NOT DELETED")
    else:
        form = DeleteEvent()
    return render(request, "DeleteEvent.html", {"form": form})


def Sell_Tickets(request):
    if(request.method == "POST"):
        form = SellTickets(request.POST)
        if(form.is_valid()):
            event_id = form.cleaned_data["eventid"]
            seat_num = form.cleaned_data["seat_num"]
            typeofticket = form.cleaned_data["typeofticket"]
            if b_SellTickets(db, event_id, typeofticket, seat_num, event_details, tickets):
                messages.success(request, "TICKET SUCCESSFULLY SOLD")
            else:
               messages.error(request, "TICKET NOT AVAILABLE")
    else:
        form = SellTickets()
    return render(request, "SellTickets.html", {"form": form})


def Cancel_Tickets(request):
    if(request.method == "POST"):
        form = CancelTicket(request.POST)
        if(form.is_valid()):
            ticket_id = form.cleaned_data["ticketid"]
            if b_CancelTicket(db, ticket_id,tickets):
                messages.success(request, "TICKET SUCCESSFULLY DELETED")
            else:
                messages.error(request, "ERROR: TICKET NOT DELETED")
    else:
        form = CancelTicket()
    return render(request, "CancelTickets.html", {"form": form})


def EditEventDetails(request):
    if(request.method == "POST"):
        form = EditEventDetailsForm(request.POST)
        if(form.is_valid()):
            eventid = form.cleaned_data["eventid"]
            artist = form.cleaned_data["artist"]
            eventtype = form.cleaned_data["event_type"]
            totaltickets = form.cleaned_data["totaltickets"]
            req = form.cleaned_data["req"]
            if b_EditEventDetails(db, eventid, artist,eventtype, totaltickets, req, event_details):
                messages.success(request, "EVENT DETAILS SUCCESSFULLY EDITED")
            else:
                messages.error(request, "EVENT NOT FOUND")
    else:
        form = EditEventDetailsForm()
    return render(request, "EditEventDetails.html", {"form": form})


def EditEventInfo(request):
    if(request.method == "POST"):
        form = EditEventInfoForm(request.POST)
        if(form.is_valid()):
            evid = form.cleaned_data["evid"]
            ven = form.cleaned_data["venue"]
            t = form.cleaned_data["time"]
            dt = form.cleaned_data["date"]
            dur = form.cleaned_data["duration"]
            if b_EditEventInfo(db, evid, ven, t, dt, dur, events_info):
                messages.success(request, "EVENT INFORMATION SUCCESSFULLY EDITED")
            else:
                messages.error(request, "EVENT NOT FOUND")
    else:
        form = EditEventInfoForm()
    return render(request, "EditEventInfo.html", {"form": form})


def EditTickets(request):
    if(request.method == "POST"):
        form = EditTicketsForm(request.POST)
        if(form.is_valid()):
            tckid = form.cleaned_data["tcktid"]
            seat_num = form.cleaned_data["seatnum"]
            typeofticket = form.cleaned_data["typeofticket"]
            if b_EditTicket(db, tckid, seat_num, typeofticket, tickets):
                messages.success(request, "TICKET SUCCESSFULLY EDITED")
            else:
                messages.error(request, "TICKET NOT FOUND")
    else:
        form = EditTicketsForm()
    return render(request, "EditTickets.html", {"form":form})

def ViewTickets(request):
    tosend = list()

    if(request.method == "POST"):
        form = ViewTicketsForm(request.POST)

        if(form.is_valid()):
            tckid = form.cleaned_data["tcktid"]
            tcktchoice = form.cleaned_data["tckts"]
            if tcktchoice == 'SOLD' or tcktchoice == 'sold':  
                if tckid in tickets:
                    temptosend = list()
                    temptosend.append("Ticket ID")
                    temptosend.append("EVENT ID")
                    temptosend.append("SEAT NUM")
                    temptosend.append("TYPE")
                    tosend.append(temptosend)  
                    for each in tickets[tckid]:
                        temptosend = list()
                        temptosend.append(each.ticket_id)
                        temptosend.append(each.event_id)
                        temptosend.append(each.seat_no)
                        temptosend.append(each.type)
                        tosend.append(temptosend)
                else:
                    messages.error(request, "NO TICKETS FOUND FOR GIVEN EVENT")

            if tcktchoice == 'AVAILABLE' or tcktchoice == 'available':
                totaltickets = 0
                for each in event_details:
                    if each.event_id == tckid:
                        totaltickets = int(each.total_tickets)
                if totaltickets != 0:
                    if tckid in tickets:
                        tosend = [['AVAILABLE TICKETS: ' + str(totaltickets - len(tickets[tckid]))]]
                    else:
                        tosend = [['AVAILABLE TICKETS: 0']]
                else:
                    messages.error(request, "EVENT DOES NOT EXIST")
    else:
        form = ViewTicketsForm()
    return render(request, "ViewTickets.html", {"form":form, "msg": tosend})


def ViewEvents(request):
    tosend = list()
    form = ViewEventsForm(request.POST)
    if form.is_valid():
        evid = form.cleaned_data["eventid"]
        eventexists = False
        for each in events_info:
            if each.event_id == evid:
                eventexists = True
                break
        if eventexists or evid == 'all' or evid == 'ALL' or evid == '-':
            tosend = b_ViewEventCatalogue(events_info, event_details, evid)
        else:
            messages.error(request, "EVENT DOES NOT EXIST")
    else:
        form = ViewEventsForm()

    return render(request, "ViewEventCatalogue.html", {"form":form, "msg": tosend})