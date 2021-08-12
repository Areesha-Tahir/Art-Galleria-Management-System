"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

# this will help us redirect to diff pages by appending in front of the url on web browser
urlpatterns = [
    path('admin/', admin.site.urls),
    path('homeadmin', views.homeadmin, name="homeadmin"),
    path('homefdo', views.homefdo, name="homefdo"),
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('AddEvent', views.AddNewEvent, name="addevent"),
    path('DeleteEvent', views.Delete_Event, name="deleteevent"),
    path('SellTicket', views.Sell_Tickets, name="sellticket"),
    path('CancelTicket', views.Cancel_Tickets, name="cancelticket"),
    path('EditEventDetails', views.EditEventDetails, name = "EditEventDetails"),
    path('EditEventInfo', views.EditEventInfo, name = "EditEventInfo"),
    path('EditTickets', views.EditTickets, name = "EditTickets"),
    path('ViewTickets', views.ViewTickets, name = "ViewTickets"),
    path('ViewEvents',views.ViewEvents,name = "ViewEvents")
]
