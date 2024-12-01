from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views
from .views import (
    HomeView,
    about_view,
    contact_view,
    ParentCreateChildCreateView,
    ParentDeleteView,
    DeleteChildView,
    delete_child,
    PupilApplicationCreateView,
    EventListView,
    staff_create_view,
    admin_dashboard
)


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"), # Home page route
    path("about/", about_view, name="aboutus"), # About us page route
    path('admissions/', views.admissions, name='admissions'),  # Admissions page route
    path('admin-login/', auth_views.LoginView.as_view(template_name='admin_login.html'), name='admin-login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admissions/form/<int:child_id>/', views.PupilApplicationCreateView.as_view(), name='admission_form'),  # Application form
    path("contact_views/", views.contact_view, name="contact"),
    path("search/", views.search_view, name="search"),
    path("contactus/", contact_view, name="contact"),
    path('staff/new/', staff_create_view, name='staff_create'),
    path('register/', views.ParentCreateChildCreateView.as_view(), name='register_parent_and_child'), # Register new parent and child
    path('school-tour/', views.school_tour, name='school_tour'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('staff/', views.staff_list, name='staff-list'),
    path('staff/<int:staff_id>/delete/', views.delete_staff, name='delete-staff'),
    path('parent/', views.parent_list, name='parent-list'),
    path('parent/<int:pk>/delete/', ParentDeleteView.as_view(), name='delete-parent'),
    path('child/', views.child_list, name='child-list'),
    path('child/<int:child_id>/delete/', delete_child, name='delete-child'),
    path('applications/', views.application_list, name='application-list'),

    # Pupil Application URLs
    path("child/<int:child_id>/application/new/", PupilApplicationCreateView.as_view(), name="pupil-application-create",
    ),  # Create a pupil application

    # ---------- Event URLs ----------
    path("events/", EventListView.as_view(), name="event-list"),  # List all events
]
