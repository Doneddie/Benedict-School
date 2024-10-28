from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="aboutus"),
    path("events/", views.EventListView.as_view(), name="events"),
    path("admissions/", views.PupilApplicationCreateView.as_view(), name="admission"),
    path("activities/", views.ActivityListView.as_view(), name="activites"),
    path("contactus/", views.ContactUsView.as_view(), name="contact"),
]
