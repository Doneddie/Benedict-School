"""
URL configuration for benedict project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import (
    ParentListView, ParentDetailView, ParentCreateView, ParentUpdateView, ParentDeleteView,
    ChildListView, ChildDetailView, ChildCreateView, ChildUpdateView, ChildDeleteView,
    PupilApplicationCreateView, PupilApplicationDetailView, 
    EventListView, EventDetailView,
    ActivityListView, ActivityDetailView
)

urlpatterns = [
    path("admin/", admin.site.urls),
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

