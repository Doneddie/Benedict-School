from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Parent, Child, PupilApplication, Exit, Event, About, Staff, GalleryImage
from django.db.models import Q
from .forms import ParentForm, ChildForm, PupilApplicationForm, ExitForm, EventForm, StaffForm, LoginForm, ContactForm, SearchForm, ChildFilterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin  # To ensure users are logged in for sensitive views
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import PermissionDenied

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Separate upcoming and past events
        current_time = timezone.now()
        context["upcoming_events"] = Event.objects.filter(date__gte=timezone.now()).order_by("date")[:3]
        context["past_events"] = Event.objects.filter(date__lt=current_time).order_by("-date")[:3]  # Latest past events first

        # Fetch the first 3 gallery images for the homepage
        context["images"] = GalleryImage.objects.all()[:3]  # Get the first 3 images
        
        return context


def school_tour(request):
    return render(request, 'contact.html')

# View for the Admissions Page
def admissions(request):
    return render(request, 'admissions.html')

# Create both parent and child
class ParentCreateChildCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        """Display the form to register both a parent and a child"""
        parent_form = ParentForm()
        child_form = ChildForm()
        return render(request, 'register_parent_and_child.html', {
            'parent_form': parent_form,
            'child_form': child_form
        })

    def form_valid(self, form):
        # Logic for saving the parent and child info
        child_id = 1

    def post(self, request, *args, **kwargs):
        """Process both the parent and child form submissions"""
        parent_form = ParentForm(request.POST, request.FILES)
        child_form = ChildForm(request.POST, request.FILES)

        if parent_form.is_valid() and child_form.is_valid():
            # Save the parent
            parent = parent_form.save()

            # Set the parent on the child form before saving
            child = child_form.save(commit=False)
            child.parent = parent  # Associate the parent with the child
            child.save()

            # Get the child_id from the saved child object
            child_id = child.id

            # Redirect to the application form for the newly created child
            return HttpResponseRedirect(reverse('pupil-application-create', kwargs={'child_id': child_id}))

        # If forms are not valid, re-render the form with errors
        return render(request, 'register_parent_and_child.html', {
            'parent_form': parent_form,
            'child_form': child_form
        })

def children_data(request):
    # Query the Child model and count the number of children per class (study_class)
    class_data = Child.objects.values('study_class').annotate(num_children=Count('study_class'))

    # Map the result to match the expected format for the chart
    # This will give us two lists: labels (class names) and data (number of children in each class)
    labels = [item['study_class'] for item in class_data]
    data = [item['num_children'] for item in class_data]

    # Return the data as JSON to the frontend
    return JsonResponse({'labels': labels, 'data': data})


# Pupil Application Views
class PupilApplicationCreateView(CreateView):
    model = PupilApplication
    form_class = PupilApplicationForm
    template_name = 'application_form.html'

    def form_valid(self, form):
        # Retrieve child_id from URL
        child_id = self.kwargs.get('child_id')

        # Get the child object (raises 404 if not found)
        child = get_object_or_404(Child, id=child_id)

        # Check if an application already exists for the given child
        existing_application = PupilApplication.objects.filter(child=child).first()

        if existing_application:
            # Option 1: Handle this by returning a message or redirecting
            return redirect('home')  # Or show a message indicating application exists.

        # If no existing application, save the new one
        application = form.save(commit=False)
        application.child = child  # Link the child to the application
        application.save()

        # Redirect to success page after form submission
        success_url = reverse_lazy('home')
        

# Event views
class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'  # Use this name in your template for easier access

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = timezone.now()
        # Separate upcoming and past events
        context["upcoming_events"] = Event.objects.filter(date__gte=current_time).order_by("date")
        context["past_events"] = Event.objects.filter(date__lt=current_time).order_by("-date")
        return context

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"] # Send email (make sure to configure your email settings in settings.py)
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            send_mail(
                subject,
                f"Message from {name} ({email}):\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Replace with your contact email
                fail_silently=False,
            )
            return render(request, "home.html")  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


#search functions views
def search_view(request):
    query = request.GET.get("q")  # Get the search query from the URL
    results = {
        "children": [],
        "staff": [],
        "events": [],
        "pages": [],  # For static pages like 'About', 'Admissions', etc.
    }

    if query:
        # Search in models
        results["children"] = Child.objects.filter(name__icontains=query)
        results["staff"] = Staff.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        results["events"] = Event.objects.filter(title__icontains=query)

        # Search in static content (e.g., pages)
        results["pages"] = About.objects.filter(content__icontains=query)  # Adjust this for any other models or static content
        results["pages"] = GalleryImage.objects.filter(cotent__icontains=query)

    return render(request, "search.html", {"results": results, "query": query})

def about_view(request):
    about_content = About.objects.first()  # Assuming a single entry for the "About" page
    
    # Filter staff members with roles 'admin', 'teacher', or 'director'
    staff_members = Staff.objects.filter(role__in=['admin', 'teacher', 'director'])
    
    context = {
        'about': about_content,
        'staff_members': staff_members,  # Pass the filtered staff members to the template
    }
    
    return render(request, 'about.html', context)


def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'images': images})

def is_admin(user):
    return user.is_authenticated and user.is_staff  # Checks if user is admin

@user_passes_test(is_admin, login_url='/admin-login/')
def admin_dashboard(request):
    # My admin view logic
    parents = Parent.objects.all()  # Get all parents from the database
    children = Child.objects.all()  # Fetch all children
    total_staff = Staff.objects.count()
    total_children = Child.objects.count()
    total_applications = PupilApplication.objects.count()

    # Pass data to the template
    context = {
        'total_staff': total_staff,
        'total_children': total_children,
        'total_applications': total_applications,
    }
    return render(request, 'admin_dashboard.html', context)
    return render(request, 'admin_dashboard.html', {'parents': parents}, {'children': children})

# Admin view to create a new staff member
@user_passes_test(is_admin, login_url='/admin-login/')
def staff_create_view(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        print("Subject received:", request.POST.get('subject_handled'))  # Debug print
        
        if form.is_valid():
            staff = form.save()
            print("Subject saved:", staff.subject_handled)  # Debug print
            messages.success(request, 'Staff member created successfully.')
            return redirect('staff_detail', pk=staff.pk)  # Changed to staff_detail
        else:
            print("Form errors:", form.errors)  # Debug print
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StaffForm()
    
    return render(request, 'staff_form.html', {
        'form': form,
        'title': 'Add New Staff Member',
        'button_text': 'Create Staff Member'
    })
    
# Staff list
@user_passes_test(is_admin, login_url='/admin-login/')
def staff_list(request):
    queryset = Staff.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query)
        )
    
    # Filters
    role = request.GET.get('role')
    if role:
        queryset = queryset.filter(role=role)
    
    # Pagination
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page')
    staff_members = paginator.get_page(page)
    
    context = {
        'staff_members': staff_members,
        'roles': Staff.ROLE_CHOICES,
    }
    
    return render(request, 'staff_list.html', context)

@property
def title(self):
    return f"Staff List - {timezone.now().strftime('%Y-%m-%d')}"

@user_passes_test(is_admin, login_url='/admin-login')
def staff_detail(request, pk):
    """
    View function for displaying detailed information about a specific staff member.
    
    Args:
        request: HttpRequest object
        pk: Primary key of the staff member
        
    Returns:
        Rendered staff detail template with staff member's information
    """
    # Get the staff member or return 404
    staff_member = get_object_or_404(Staff, pk=pk)
    
    # Get a subject for teaching staff
    subject = None
    if staff_member.is_teaching_staff and staff_member.subject_handled:
    # Format it as a list of dicts to match your template's expectation
        subjects = [{'name': staff_member.get_subject_handled_display()}]
    else:
        subjects = []
    
    # Get contact information
    contact_info = staff_member.get_contact_info()
    
    # Calculate age from date_of_birth
    age = None
    if staff_member.date_of_birth:
        today = timezone.now().date()
        age = today.year - staff_member.date_of_birth.year - (
            (today.month, today.day) < 
            (staff_member.date_of_birth.month, staff_member.date_of_birth.day)
        )
    
    context = {
        'staff_member': staff_member,
        'subjects': subjects,
        'contact_info': contact_info,
        'age': age,
    }
    
    return render(request, 'staff_detail.html', context)

# Delete staff
@user_passes_test(is_admin, login_url='/admin-login/')
def staff_delete(request, pk):
    # Get the staff member by primary key (pk)
    staff_member = get_object_or_404(Staff, pk=pk)
    
    # If the request method is POST, handle the deletion
    if request.method == 'POST':
        staff_member.delete()  # Delete the staff member
        messages.success(request, 'Staff member deleted successfully.')
        return redirect(reverse('staff_list'))  # Redirect to the staff list view
    
    # If GET request, display the confirmation page
    return render(request, 'staff_confirm_delete.html', {'staff_member': staff_member})

# Parent views
@user_passes_test(is_admin, login_url='/admin-login/')
def parent_list(request):
    # Get all parents initially
    parent_list = Parent.objects.all().order_by('first_name')
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        parent_list = parent_list.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(ID_number__icontains=search_query)
        )

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(parent_list, 10)  # Show 10 parents per page
    
    try:
        parents = paginator.page(page)
    except PageNotAnInteger:
        parents = paginator.page(1)
    except EmptyPage:
        parents = paginator.page(paginator.num_pages)

    context = {
        'parents': parents,
        'page_obj': parents,  # For compatibility with your template
        'is_paginated': parents.has_other_pages(),
        'search_query': search_query,
    }

    return render(request, 'parent_list.html', context)

    @property
    def title(self):
        return f"Parent List - {timezone.now().strftime('%Y-%m-%d')}"

@user_passes_test(is_admin, login_url='/admin-login/')
def delete_parent(request, pk):  # Added pk parameter here
    parent = get_object_or_404(Parent, pk=pk)
    
    if request.method == 'POST':
        parent.delete()
        messages.success(request, 'Parent deleted successfully')
        return redirect('parent-list')
        
    context = {
        'parent': parent,
        'children': parent.children.all()  # Using the related_name we fixed earlier
    }
    return render(request, 'parent_confirm_delete.html', context)

# Child views

@user_passes_test(is_admin, login_url='/admin-login/')
def child_list(request):
    # Instantiate the filter form and populate it with GET data
    form = ChildFilterForm(request.GET)
    
    # Start with the full queryset of Child objects
    queryset = Child.objects.all()

    # Apply filters if the form is valid
    if form.is_valid():
        # Search filter
        search_query = form.cleaned_data.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Sex filter
        sex = form.cleaned_data.get('sex')
        if sex:
            queryset = queryset.filter(sex=sex)

        # Class filter
        study_class = form.cleaned_data.get('study_class')
        if study_class:
            queryset = queryset.filter(study_class=study_class)

        # Age filter
        age_range = form.cleaned_data.get('age_range')
        if age_range:
            today = datetime.now().date()
            if age_range == '0-3':
                max_date = today.replace(year=today.year - 0)
                min_date = today.replace(year=today.year - 3)
                queryset = queryset.filter(date_of_birth__range=[min_date, max_date])
            elif age_range == '4-6':
                max_date = today.replace(year=today.year - 4)
                min_date = today.replace(year=today.year - 6)
                queryset = queryset.filter(date_of_birth__range=[min_date, max_date])
            elif age_range == '7-9':
                max_date = today.replace(year=today.year - 7)
                min_date = today.replace(year=today.year - 9)
                queryset = queryset.filter(date_of_birth__range=[min_date, max_date])
            elif age_range == '10+':
                max_date = today.replace(year=today.year - 10)
                queryset = queryset.filter(date_of_birth__lte=max_date)

    # Pagination
    paginator = Paginator(queryset, 10)  # Paginate by 10
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context for the template
    context = {
        'filter_form': form,
        'children': page_obj,
    }

    # Render the child list template with the form and the paginated queryset
    return render(request, 'child_list.html', context)

    @property
    def title(self):
        return f"Child List - {timezone.now().strftime('%Y-%m-%d')}"

@user_passes_test(is_admin, login_url='/admin-login/')
def delete_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    child.delete()
    return redirect('child-list')

# Application view
@user_passes_test(is_admin, login_url='/admin-login/')
def application_list(request):
    applications = PupilApplication.objects.select_related('child').all()
    return render(request, 'application_list.html', {'applications': applications})

    # Pagination
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page')
    staff_members = paginator.get_page(page)

@user_passes_test(is_admin, login_url='/admin-login/')
def alumni_list(request):
    alumni_parents = Parent.objects.filter(status='alumni').order_by('-alumni_date')
    alumni_children = Child.objects.filter(status='alumni').order_by('-alumni_date')
    
    context = {
        'alumni_parents': alumni_parents,
        'alumni_children': alumni_children,
    }
    
    return render(request, 'alumni_list.html', context)

@user_passes_test(is_admin, login_url='/admin-login/')
def child_to_alumni(request, pk):
    """Move individual child to alumni status"""
    child = get_object_or_404(Child, pk=pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        child.move_to_alumni(reason)
        
        # Check if parent was moved to alumni
        if child.parent.status == 'alumni':
            messages.success(request, 
                f'{child.name} moved to alumni. Parent {child.parent.first_name} '
                'also moved to alumni as no active students remain.')
        else:
            messages.success(request, 
                f'{child.name} moved to alumni. Parent remains active with '
                f'{child.parent.get_child_count()["active"]} active children.')
        
        return redirect('child-list')
        
    context = {
        'child': child,
        'parent': child.parent,
        'siblings': child.parent.children.exclude(pk=child.pk)
    }
    return render(request, 'child_to_alumni_confirm.html', context)

@user_passes_test(is_admin, login_url='/admin-login/')
def parent_to_alumni(request, pk):
    """Move parent and all children to alumni status"""
    parent = get_object_or_404(Parent, pk=pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        
        # First check if there are active children
        if parent.has_active_children():
            messages.error(request, 
                'Cannot move parent to alumni while they have active children. '
                'Please move children to alumni first.')
            return redirect('parent-list')
            
        parent.move_to_alumni(reason)
        messages.success(request, 
            f'{parent.first_name} {parent.last_name} moved to alumni status.')
        return redirect('parent-list')
        
    context = {
        'parent': parent,
        'active_children': parent.children.filter(status='active'),
        'alumni_children': parent.children.filter(status='alumni')
    }
    return render(request, 'parent_to_alumni_confirm.html', context)



