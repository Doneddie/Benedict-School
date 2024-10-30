from django import forms
from .models import Staff, Event,Activity, PupilApplication,Child, Exit,Parent


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search...', 'class': 'form-control'})
    )


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "subjects_handled",
            "years_of_experience",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "subjects_handled": forms.Select(attrs={"class": "form-control"}),
            "years_of_experience": forms.NumberInput(attrs={"class": "form-control"}),
        }


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = [
            "Username",
            "password",
            "ID_number",
            "email",
            "address",
            "profile_image",
        ]
        widgets = {
            "password": forms.PasswordInput(),  # Use password input for the password field
        }


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = [
            "parent",
            "name",
            "date_of_birth",
            "profile_image",
            "application_status",
        ]


class PupilApplicationForm(forms.ModelForm):
    class Meta:
        model = PupilApplication
        fields = ["child", "documents", "notes"]


class ExitForm(forms.ModelForm):
    class Meta:
        model = Exit
        fields = ["child", "exit_date", "reason"]


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["title", "description", "date"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "location", "description", "image", "video"]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    subject = forms.CharField(max_length=100, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")
