# 1. Django core imports (alphabetical by module)
from django.urls import path
from django.views.generic.base import RedirectView

# 2. Django contrib imports (group auth-related together)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.storage import staticfiles_storage

# 3. Local imports (specific imports first, then wildcards)
from .views import (
    HomeView,
    about_view,
    admin_dashboard,
    contact_view,
    delete_child,
    EventListView,
    ParentCreateView,
    pupil_application_detail,
    register_children,
    search_view,
    staff_create_view,
    staff_delete,
    staff_list,
)
from . import views

urlpatterns = [
    # --------------------------
    # Basic Pages & Public Routes
    # --------------------------
    path("", views.HomeView.as_view(), name="home"),
    path("about/", about_view, name="about"),
    path('school-tour/', views.school_tour, name='school-tour'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('admissions/', views.admissions, name='admissions'),

    # --------------------------
    # Authentication & Admin
    # --------------------------
    path('admin-login/', auth_views.LoginView.as_view(template_name='admin_login.html'), name='admin-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),

    # --------------------------
    # Contact & Search
    # --------------------------
    path("contact/", contact_view, name="contact"), 
    path("search/", views.search_view, name="search"),

    # --------------------------
    # Parent Management
    # --------------------------
    path('parents/', views.parent_list, name='parent-list'),
    path('parent/create/', ParentCreateView.as_view(), name='parent-create'),
    path('parent/<int:pk>/delete/', views.delete_parent, name='parent-delete'),
    path('parent/<int:pk>/to-alumni/', views.parent_to_alumni, name='parent-to-alumni'),

    # --------------------------
    # Child Management
    # --------------------------
    path('children/', views.child_list, name='child-list'),
    path('child/<int:pk>/delete/', delete_child, name='child-delete'),
    path('child/<int:pk>/to-alumni/', views.child_to_alumni, name='child-to-alumni'),
    path('register/<int:parent_id>/', views.register_children, name='register-children'),

    # --------------------------
    # Staff Management
    # --------------------------
    path('staff/', views.staff_list, name='staff-list'),
    path('staff/create/', views.staff_create_view, name='staff-create'),
    path('staff/<int:pk>/', views.staff_detail, name='staff-detail'),
    path('staff/<int:pk>/delete/', views.staff_delete, name='staff-delete'),

    # --------------------------
    # Applications & Admissions
    # --------------------------
    path('applications/', views.application_list, name='application-list'),
    path('applications/<int:pk>/', pupil_application_detail, name='application-detail'),

    # --------------------------
    # Events & Gallery
    # --------------------------
    path("events/", EventListView.as_view(), name="event-list"),
    path('gallery/', views.gallery, name='gallery'),

    # --------------------------
    # Alumni Management
    # --------------------------
    path('alumni/', views.alumni_list, name='alumni-list'),

    # --------------------------
    # Admin Dashboard API Endpoints
    # --------------------------
    path('admin-dashboard/api/children-data/', views.children_data, name='children-data'),
    path('admin-dashboard/api/gender-distribution/', views.gender_distribution, name='gender-distribution'),
    path('admin-dashboard/api/alumni-distribution/', views.alumni_distribution, name='alumni-distribution'),

    # --------------------------
    # Static Assets
    # --------------------------
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]
