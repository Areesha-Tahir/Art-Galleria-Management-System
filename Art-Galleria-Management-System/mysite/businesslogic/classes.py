# ========================================================================================================
#       CLASSES NEEDED BY THE BUSINESS LOGIC LAYER
# ========================================================================================================

# We will have an array to store each attribute of each classes

class Event_Specification:  # Admin
    def __init__(self, id, v, t, dt, dur):
        self.event_id = id
        self.venue = v
        self.time = t
        self.date = dt
        self.duration = dur

    def event_print(self):
        print( self.event_id, end = ", ")
        print( self.venue, end = ", ")
        print( self.time, end = ", ")
        print( self.date, end = ", ")
        print( self.duration)

    def returnInfo(self):
        returnStr = self.event_id + " "
        returnStr += self.venue + " "
        returnStr += self.time + " "
        returnStr += self.date + " "
        returnStr += self.duration
        return returnStr 

    def UpdateEventSpecs(self, v, t, dt, dur):
        self.venue = v
        self.time = t
        self.date = dt
        self.duration = dur


class Event_Details:  # Event_Manager
    def __init__(self, id, art, ty, av_tckts, req):
        self.event_id = id
        self.artist = art
        self.event_type = ty
        self.total_tickets = av_tckts
        self.specific_requirement = req

    def returnDetails(self):
        returnStr = self.event_id + " "
        returnStr += self.artist + " "
        returnStr += self.event_type + " "
        returnStr += self.total_tickets + " "
        returnStr += self.specific_requirement
        return returnStr

    def event_print(self):
        print( self.event_id, end = ", ")
        print( self.artist, end = ", ")
        print( self.event_type, end = ", ")
        print( self.total_tickets, end = ", ")
        print( self.specific_requirement)

    def UpdateEventDetails(self, art, ty, av_tckts, req):
        self.artist = art
        self.event_type = ty
        self.total_tickets = av_tckts
        self.specific_requirement = req


def Display(event_details, event_specification):
    returnStr = list()
    returnStr.append( "Event ID : " + event_specification.event_id)
    returnStr.append( "Venue : " + event_specification.venue)
    returnStr.append("Time : " + event_specification.time )
    returnStr.append("Duration : " + event_specification.duration)
    returnStr.append( "Artist : " + event_details.artist)
    returnStr.append( "Event Type : " + event_details.event_type)
    returnStr.append("Total Tickets : " + event_details.total_tickets)
    returnStr.append("Specfic Requirement : " + event_details.specific_requirement)

    return returnStr
    

class Ticket:
    def __init__(self, t_id, ev_id, st, ty):
        self.ticket_id = t_id
        self.event_id = ev_id
        self.seat_no = st
        self.type = ty

    def returnTickets(self):
        returnStr = self.ticket_id + " "
        returnStr += self.event_id + " "
        returnStr += self.seat_no + " "
        returnStr += self.type + " "
        return returnStr

    def ticket_print(self):
        print( self.event_id, end = ", ")
        print( self.ticket_id, end = ", ")
        print( self.seat_no, end = ", ")
        print( self.type)

    def UpdateTickets(self, st, ty):
        self.seat_no = st
        self.type = ty


class BackstagePersonnel:
    def __init__(self, ev_id, name, cnic, jb, b_id):
        self.event_id = ev_id
        self.name = name
        self.cnic = cnic
        self.job = jb
        self.backstage_id = b_id


class User_Details:
    def __init__(self, name, cnic, addr, email, ph, jb, u_id):
        self.name = name
        self.cnic = cnic
        self.address = addr
        self.email = email
        self.phone_number = ph
        self.user_id = u_id


class User_Accounts:
    def __init__(self, u_id, passw):
        self.user_id = u_id
        self.password = passw
