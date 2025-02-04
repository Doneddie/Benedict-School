from django import forms
from datetime import date
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.layout import HTML
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from crispy_forms.helper import FormHelper
from .models import Parent, Child, PupilApplication, Staff, Event, Exit


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
    """Form for creating and updating staff members""" 
    class Meta:
        model = Staff
        fields = [
            # Personal Information
            'name', 'sex', 'date_of_birth', 'ID_number', 'email', 
            'tel_no', 'photo', 'address',
            
            # Emergency Contact
            'emergency_contact_name', 'emergency_contact_relationship', 
            'emergency_contact_phone',
            
            # Employment Information
            'role', 'employee_id',
            
            # Qualification Information
            'qualification', 'certificates', 'years_of_experience',
            
            # Teaching Staff Information
            'class_name', 'subject_handled',
            
            # Non-teaching Staff Information
            'department', 
            
            # Salary Information
            'salary', 'bank_account_name', 'bank_account_number', 'bank_name'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'qualification': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-9'
        
        # Dynamic form handling based on role
        if 'role' in self.data:
            self.show_fields_for_role(self.data['role'])
        elif self.instance.pk:
            self.show_fields_for_role(self.instance.role)
        
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('role', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                css_class='mb-3'
            ),
            Div(
                HTML("<h2>Personal Information</h2>"),
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    Column('sex', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('date_of_birth', css_class='form-group col-md-6 mb-0'),
                    Column('ID_number', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('email', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('tel_no', css_class='form-group col-md-6 mb-0'),
                    Column('employee_id', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                'photo',
                'address',
                css_class='mb-3'
            ),
            Div(
                HTML("<h2>Emergency Contact</h2>"),
                Row(
                    Column('emergency_contact_name', css_class='form-group col-md-6 mb-0'),
                    Column('emergency_contact_relationship', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                'emergency_contact_phone',
                css_class='mb-3'
            ),
            Div(
                HTML("<h2>Qualifications</h2>"),
                'qualification',
                'certificates',
                'years_of_experience',
                css_class='mb-3'
            ),
            Div(
                HTML("<h2>Teaching Information</h2>"),
                Row(
                    Column('class_name', css_class='form-group col-md-6 mb-0'),
                    Column('subject_handled', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                css_class='mb-3 teaching-fields'
            ),
            Div(
                HTML("<h2>Non-Teaching Information</h2>"),
                Row(
                    Column('department', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                css_class='mb-3 non-teaching-fields'
            ),
            Div(
                HTML("<h2>Salary Information</h2>"),
                Row(
                    Column('salary', css_class='form-group col-md-6 mb-0'),
                    Column('bank_name', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('bank_account_name', css_class='form-group col-md-6 mb-0'),
                    Column('bank_account_number', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                css_class='mb-3'
            ),
            Submit('submit', _('Save Staff Member'), css_class='btn btn-primary')
        )

    def show_fields_for_role(self, role):
        """Show/hide fields based on staff role"""
        teaching_roles = ["teacher"]
        is_teaching = role in teaching_roles
        
        # Teaching staff fields
        for field in ['class_name', 'subject_handled']:
            if field in self.fields:
                self.fields[field].required = is_teaching
                if not is_teaching:
                    self.fields[field].widget = forms.HiddenInput()
        
        # Non-teaching staff fields
        for field in ['department']:
            if field in self.fields:
                self.fields[field].required = not is_teaching
                if is_teaching:
                    self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        """
        Custom form validation
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        role = cleaned_data.get('role')
        
        # Role-specific validation
        if role in ["teacher"]:
            if not cleaned_data.get('class_name'):
                raise ValidationError(_("Teaching staff must be assigned to a class."))
            if not cleaned_data.get('subject_handled'):
                raise ValidationError(_("Teaching staff must have a subject assigned."))
        else:
            if not cleaned_data.get('department'):
                raise ValidationError(_("Non-teaching staff must be assigned to a department."))
        
        return cleaned_data

    class Media:
        js = (
            'js/staff_form.js',  # created this JavaScript file
        )

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = [
            'first_name', 'last_name', 'relationship_type', 'sex', 
            'ID_number', 'email', 'tel_no', 'address', 
            'parent_image'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tel_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

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

class ParentFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name...'
        })
    )

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['full_name', 'date_of_birth', 'sex', 'study_class', 'profile_image']
    
    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)  # Get parent from kwargs
        super().__init__(*args, **kwargs)  # Call the parent class's __init__ method
        
        # If parent is provided, you can set any logic you need (like setting initial values)
        if parent:
            self.parent = parent

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        
        if date_of_birth > date.today():
            raise ValidationError("Date of birth cannot be in the future.")
        
        return date_of_birth

class ChildFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name...'
        })
    )
    
    sex = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + Child.sex.field.choices,  # Include blank option for "All"
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    study_class = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + Child.study_class.field.choices,  # Include blank option for "All"
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    age_range = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Ages'),
            ('0-3', '0-3 years'),
            ('4-6', '4-6 years'),
            ('7-9', '7-9 years'),
            ('10+', '10+ years')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class ParentChildFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instances = super().save(commit=False)
        for instance in instances:
            instance.parent = self.parent
            instance.save()
        return instances

class PupilApplicationForm(forms.ModelForm):
    class Meta:
        model = PupilApplication
        fields = [
            'documents', 
            'allergies', 
            'allergy_details', 
            'medical_conditions', 
            'emergency_contact_name', 
            'emergency_contact_phone', 
            'special_needs', 
            'previous_school', 
            'notes'
        ]


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
    









