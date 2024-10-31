from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="aboutus"),
    path("admissions/", views.PupilApplicationCreateView.as_view(), name="admission"),
    path("activities/", views.ActivityListView.as_view(), name="activites"),
    path("contactus/", views.ContactUsView.as_view(), name="contact"),
    path("login/", views.LoginViews.as_views, name = "login"),

    # parent urls
    path('parents/', ParentListView.as_view(), name='parent-list'),  # List all parents
    path('parent/<int:pk>/', ParentDetailView.as_view(), name='parent-detail'),  # Parent detail page
    path('parent/new/', ParentCreateView.as_view(), name='parent-create'),  # Create a new parent
    path('parent/<int:pk>/edit/', ParentUpdateView.as_view(), name='parent-update'),  # Edit a parent
    path('parent/<int:pk>/delete/', ParentDeleteView.as_view(), name='parent-delete'),  # Delete a parent

    # child urls
    path('parent/<int:parent_id>/children/', ChildListView.as_view(), name='child-list'),  # List all children for a parent
    path('parent/<int:parent_id>/child/new/', ChildCreateView.as_view(), name='child-create'),  # Create a new child
    path('child/<int:pk>/', ChildDetailView.as_view(), name='child-detail'),  # Child detail page
    path('child/<int:pk>/edit/', ChildUpdateView.as_view(), name='child-update'),  # Edit a child
    path('child/<int:pk>/delete/', ChildDeleteView.as_view(), name='child-delete'),  # Delete a child

    # Pupil Application URLs
    path('child/<int:child_id>/application/new/', PupilApplicationCreateView.as_view(), name='pupil-application-create'),  # Create a pupil application
    path('application/<int:pk>/', PupilApplicationDetailView.as_view(), name='pupil-application-detail'),  # View a specific pupil application

    # ---------- Event URLs ----------
    path('events/', EventListView.as_view(), name='event-list'),  # List all events
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),  # Event detail page

    # ---------- Activity URLs ----------
    path('activities/', ActivityListView.as_view(), name='activity-list'),  # List all activities
    path('activity/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),  # Activity detail page
]
