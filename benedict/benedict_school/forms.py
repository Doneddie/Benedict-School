from django import forms
from .models import Staff

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
        fields = ['name', 'position', 'profile_image', 'subjects_handled', 'years_of_experience']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Staff Name', 'class': 'form-control'}),
            'position': forms.TextInput(attrs={'placeholder': 'Position', 'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'subjects_handled': forms.TextInput(attrs={'placeholder': 'Subjects Handled (comma-separated)', 'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'placeholder': 'Years of Experience', 'class': 'form-control'}),
        }
