from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django import forms
from .models import Parent, Child, PupilApplication, Staff, Event, Exit 
from datetime import date


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
            "name",
            "ID_number",
            "email",
            "tel_no",
            "class_name",
            "subjects_handled",
            "years_of_experience",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "ID_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "tel_no": forms.TextInput(attrs={"class": "form-control"}),
            "class_name": forms.TextInput(attrs={"class": "form-control"}),
            "subjects_handled": forms.Select(attrs={"class": "form-control"}),
            "years_of_experience": forms.NumberInput(attrs={"class": "form-control"}),
        }


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'ID_number', 'email', 'tel_no', 'address', 'parent_image']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Ensure that the email address is unique
        if Parent.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        
        # Validate the format of the email
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address.")
        
        return email
    
    def clean_ID_number(self):
        ID_number = self.cleaned_data.get('ID_number')
        
        # Ensure that the ID_number is unique
        if Parent.objects.filter(ID_number=ID_number).exists():
            raise ValidationError("This ID number is already registered.")
        # Check the length of ID number     

        if len(ID_number) != 14:
            raise ValidationError("ID number should be 14 characters long.")
        
        return ID_number

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'date_of_birth', 'study_class', 'profile_image', 'application_status']
        date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'})
    )

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        
        if date_of_birth > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        
        return date_of_birth

class PupilApplicationForm(forms.ModelForm):
    class Meta:
        model = PupilApplication
        fields = ['documents', 'notes']

    def clean_documents(self):
        documents = self.cleaned_data.get('documents')

        if documents:
            # File size validation: Limit to 5MB (5 * 1024 * 1024)
            max_size = 5 * 1024 * 1024  # 5 MB
            if documents.size > max_size:
                raise ValidationError("The document size exceeds the 5MB limit.")

            # File type validation: Allow only PDF or DOCX
            allowed_extensions = ['pdf','docx']
            file_extension = documents.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError("Only PDF or DOCX files are allowed.")
        
        return documents
        
        if documents:
            # Check the size and type if a document is uploaded
            ...
        else:
            # You can handle the case where no file is uploaded if needed
            pass

    def clean_notes(self):
        notes = self.cleaned_data.get('notes')
       
        return notes

class ExitForm(forms.ModelForm):
    class Meta:
        model = Exit
        fields = ["child", "exit_date", "reason"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "date", "location", "description", "image", "video"]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email Address")
    subject = forms.CharField(max_length=100, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")

    # Added custom validation or clean methods
    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message
    









