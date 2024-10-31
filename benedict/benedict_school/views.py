from django.shortcuts import render
from django.http import HttpResponse


# I am creating my views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from .models import Parent, Child, PupilApplication, Exit, Activity, Event
from .forms import ParentForm, ChildForm, PupilApplicationForm, ExitForm, ActivityForm, EventForm, StaffForm,LoginForm, ContactForm,SearchForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin  # To ensure users are logged in for sensitive views
from django.utils import timezone


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Retrieve all activities and events from the database
        context["activities"] = Activity.objects.all()  # Get all activities
        context["events"] = Event.objects.filter(date__gte=timezone.now()).order_by(
            "date"
        )  # Get upcoming events

        return context


# Parent views
class ParentListView(ListView):
    model = Parent
    template_name = 'parents/parent_list.html'
    context_object_name = 'parents'

class ParentDetailView(DetailView):
    model = Parent
    template_name = 'parents/parent_detail.html'
    context_object_name = 'parent'

class ParentCreateView(CreateView):
    model = Parent
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    fields = ['Username', 'password', 'ID_number', 'email', 'address', 'profile_image']
    success_url = reverse_lazy('parent-list')  # Redirect to parent list after creating a new parent

class ParentUpdateView(UpdateView):
    model = Parent
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    fields = ['Username', 'password', 'ID_number', 'email', 'address', 'profile_image']
    success_url = reverse_lazy('parent-list')

class ParentDeleteView(DeleteView):
    model = Parent
    template_name = 'parents/parent_confirm_delete.html' # Confirmation before deletion
    success_url = reverse_lazy('parent-list')

# Child views

class ChildListView(ListView):
    model = Child
    template_name = 'children/child_list.html'
    context_object_name = 'children'

    def get_queryset(self):
        """Override to filter children by their parent"""
        parent = get_object_or_404(Parent, id=self.kwargs['parent_id'])
        return Child.objects.filter(parent=parent)

class ChildDetailView(DetailView):
    model = Child
    template_name = 'children/child_detail.html'
    context_object_name = 'child'

class ChildCreateView(CreateView):
    model = Child
    form_class = ChildForm
    template_name = 'children/child_form.html'
    fields = ['name', 'date_of_birth', 'profile_image', 'application_status']

    def form_valid(self, form):
        """Set the parent before saving the child"""
        parent = get_object_or_404(Parent, id=self.kwargs['parent_id'])
        form.instance.parent = parent
        return super().form_valid(form)
    
    success_url = reverse_lazy('child-list')

class ChildUpdateView(UpdateView):
    model = Child
    form_class = ChildForm
    template_name = 'children/child_form.html'
    fields = ['name', 'date_of_birth', 'profile_image', 'application_status']
    success_url = reverse_lazy('child-list')

class ChildDeleteView(DeleteView):
    model = Child
    template_name = 'children/child_confirm_delete.html' # Confirmation before deletion
    success_url = reverse_lazy('child-list')

# Pupil Application Views

class PupilApplicationDetailView(DetailView):
    model = PupilApplication
    template_name = 'applications/application_detail.html'
    context_object_name = 'application'

class PupilApplicationCreateView(CreateView):
    model = PupilApplication
    form_class = PupilApplicationForm
    template_name = 'applications/application_form.html'
    fields = ['documents', 'notes']

    def form_valid(self, form):
        """Set the child before saving the application"""
        child = get_object_or_404(Child, id=self.kwargs['child_id'])
        form.instance.child = child
        return super().form_valid(form)
    
    success_url = reverse_lazy('application-list')

# Event views
class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'

# Activity views
class ActivityListView(ListView):
    model = Activity
    template_name = 'activity_list.html'

class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity_detail.html'


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email (make sure to configure your email settings in settings.py)
            name = form.cleaned_data["name"]
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
