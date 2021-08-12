from django import forms


class LoginForm(forms.Form):
    Name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))


class AddEvent(forms.Form):
    venue = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    time = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    duration = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input'}))


class SellTickets(forms.Form):
    eventid = forms.CharField(label="Event ID ", max_length=50)
    typeofticket = forms.CharField(label="Type ", max_length=100)
    seat_num = forms.CharField(label="Seat # ", max_length=100)


class DeleteEvent(forms.Form):
    eventid = forms.CharField(label="Event ID", max_length=50)


class CancelTicket(forms.Form):
    ticketid = forms.CharField(label="Ticket ID", max_length=50)

class EditEventDetailsForm(forms.Form):
    eventid = forms.CharField(label="Event ID ", max_length=50)
    artist = forms.CharField(label="Artist ", max_length=100)
    event_type = forms.CharField(label="Event Type ", max_length=100)
    totaltickets = forms.CharField(label="Total Tickets ", max_length=100)
    req = forms.CharField(label="Requirements ", max_length=100)

class EditEventInfoForm(forms.Form):
    evid = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    venue = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    time = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    duration = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))

class EditTicketsForm(forms.Form):
    tcktid = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    typeofticket = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    seatnum = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))

class ViewTicketsForm(forms.Form):
    CHOICES = [('sold', 'SOLD'),('available', 'AVAILABLE')]
    tckts = forms.CharField(label='Ticket Category: ', widget=forms.RadioSelect(choices=CHOICES))
    tcktid = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))

class ViewEventsForm(forms.Form):
    eventid = forms.CharField(label="Event ID", max_length=50)