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
from .forms import ParentForm, ChildForm, PupilApplicationForm, ExitForm, EventForm, StaffForm, LoginForm, ContactForm, SearchForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin  # To ensure users are logged in for sensitive views
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Count

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Separate upcoming and past events
        current_time = timezone.now()
        context["upcoming_events"] = Event.objects.filter(date__gte=timezone.now()).order_by("date")
        context["past_events"] = Event.objects.filter(date__lt=current_time).order_by("-date")  # Latest past events first

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

class ParentDeleteView(DeleteView):
    model = Parent
    template_name = 'parent_confirm_delete.html'  # Custom delete confirmation template
    context_object_name = 'parent'  # Context name for the parent instance
    success_url = reverse_lazy('parent-list')  # Redirect after successful delete

    def get_queryset(self):
        """
        Ensure that only superusers or admins can delete parents.
        """
        return Parent.objects.all()  # You can filter here if needed based on user permissions

class DeleteChildView(DeleteView):
    model = Child
    template_name = 'child_confirm_delete.html'  # Custom template for confirmation
    context_object_name = 'child'
    success_url = reverse_lazy('child-list')  # Redirect after successful delete

    def get_queryset(self):
        """
        This can be adjusted to ensure only admins can delete children.
        """
        return Child.objects.all()

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
    return render(request, 'about.html', {'about': about_content})

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
        if form.is_valid():
            staff = form.save()
            messages.success(request, 'Staff member created successfully.')
            return redirect('staff_detail', pk=staff.pk)
    else:
        form = StaffForm()
    
    return render(request, 'staff_form.html', {
        'form': form,
        'title': 'Add New Staff Member',
        'button_text': 'Create Staff Member'
    })
# Staff list
@user_passes_test(is_admin, login_url='/admin-login/')
class StaffListView(ListView):
    model = Staff
    template_name = 'staff_list.html'
    context_object_name = 'staff_members'
    paginate_by = 10

    def get_queryset(self):
        queryset = Staff.objects.all()
        # Filter by role if specified
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = Staff.ROLE_CHOICES
        return context
# Delete staff
@user_passes_test(is_admin, login_url='/admin-login/')
class StaffDeleteView:
    model = Staff
    template_name = 'staff_confirm_delete.html'
    success_url = reverse_lazy('staff_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Staff member deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Parent views
@user_passes_test(is_admin, login_url='/admin-login/')
def parent_list(request):
    parents = Parent.objects.all()
    return render(request, 'parent_list.html', {'parents': parents})

@user_passes_test(is_admin, login_url='/admin-login/')
def delete_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    parent.delete()
    return redirect('parent-list')

# Child views

@user_passes_test(is_admin, login_url='/admin-login/')
def child_list(request):
    children = Child.objects.all()
    return render(request, 'child_list.html', {'children': children})

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



