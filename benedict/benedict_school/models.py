from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


class Parent(models.Model): 
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='') 
    ID_number = models.CharField(max_length=14, unique=True, null=False, default='')
    email = models.EmailField(unique=True)
    tel_no = models.CharField(max_length=15, default='') 
    address = models.CharField(max_length=100)
    parent_image = models.ImageField(
        upload_to="parent_images/", null=True, blank=True
    )

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('alumni', 'Alumni'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    alumni_date = models.DateTimeField(null=True, blank=True)
    reason_for_leaving = models.TextField(blank=True, null=True)

    def move_to_alumni(self, reason=''):
        """Only move parent to alumni if all children are alumni"""
        if not self.has_active_children():
            self.status = 'alumni'
            self.alumni_date = timezone.now()
            self.reason_for_leaving = reason
            self.save()
            return True
        return False

    def has_active_children(self):
        """Check if parent has any active children"""
        return self.children.filter(status='active').exists()

    def get_child_count(self):
        """Get count of total and active children"""
        total = self.child.count()
        active = self.child.filter(status='active').count()
        return {'total': total, 'active': active}

            
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Child(models.Model):
    parent = models.ForeignKey(
        Parent, on_delete=models.CASCADE, related_name="children"
    )
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=10, choices=[ ("male", "Male"), ("female", "Female")], default="male",)
    study_class = models.CharField(
        max_length=20, 
        choices=[
            ("baby_class", "Baby Class"),
            ("middle_class", "Middle class"),
            ("top_class", "Top class"),
            ("primary_one", "Primary one"),
            ("primary_two", "Primary two"),
            ("primary_three", "Primary three"),
            ("primary_four", "Primary four")
        ],
        default="primary_one",
    )

    profile_image = models.ImageField(upload_to="child_images/", null=True, blank=True)

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('alumni', 'Alumni'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    alumni_date = models.DateTimeField(null=True, blank=True)
    reason_for_leaving = models.TextField(blank=True, null=True)

    def move_to_alumni(self, reason=''):
        """Move child to alumni status and check parent"""
        self.status = 'alumni'
        self.alumni_date = timezone.now()
        self.reason_for_leaving = reason
        self.save()
        
        # Check if parent should be moved to alumni (no active children left)
        if not self.parent.has_active_children():
            self.parent.move_to_alumni(reason)

    def __str__(self):
        return self.name


class PupilApplication(models.Model):
    child = models.OneToOneField(Child, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    documents = models.FileField(upload_to="applications/", null=True, blank=True)
    notes = models.TextField(null=True, blank=True)  # Filled by administrator

    def __str__(self):
        return f"Application for {self.child.name}"

    
class Exit(models.Model): 
    child = models.ForeignKey(Child, on_delete=models.CASCADE) 
    exit_date = models.DateField() 
    reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.child.name} left on {self.exit_date}"


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to="event_images/", null=True, blank=True
    )  # For event images
    video = models.FileField(
        upload_to="event_videos/", null=True, blank=True
    )  # For event videos

    def __str__(self):
        return self.title


class Staff(models.Model):
    """
    Staff model for both teaching and non-teaching staff members.
    Includes comprehensive personal information and role-specific fields.
    """
    
    # Role Choices
    ROLE_CHOICES = [
        ("teacher", "Teacher"),
        ("director", "Director"),
        ("cleaner", "Cleaner"),
        ("cook", "Cook"),
        ("admin", "Admin Staff"),
        ("librarian", "Librarian"),
        ("nurse", "School Nurse"),
        ("security", "Security"),
        ("other", "Other")
    ]

    # Class Choices
    CLASS_CHOICES = [
        ('nursery', 'Nursery'),
        ('primary_1', 'Primary One'),
        ('primary_2', 'Primary Two'),
        ('primary_3', 'Primary Three'),
        ('primary_4', 'Primary Four'),
        ('primary_5', 'Primary Five'),
        ('primary_6', 'Primary Six'),
    ]

    # Subejct Choices
    SUBJECT_CHOICES = [
        ('english', 'English'),
        ('mathematics', 'Mathematics'),
        ('science', 'Science'),
        ('social_studies', 'Social Studies'),
        ('literacy', 'Literacy'),
        ('literacy_1', 'Literacy 1'),
        ('literacy_1a', 'Literacy 1A'),
        ('literacy_1b', 'Literacy 1B'),
        ('religous_education', 'Religous Education'),
        ('reading', 'Reading'),
        ('luganda', 'Luganda'),
        ('learning_area_1_5', 'Learing Area 1-5')
    ]

    # Department Choices
    DEPARTMENT_CHOICES = [
        ('administration', 'Administration'),
        ('kitchen', 'Kitchen'),
        ('security', 'Security'),
        ('medical', 'Medical'),
        ('library', 'Library'),
        ('other', 'Other')
    ]

    # Validators
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    id_validator = RegexValidator(
        regex=r'^[A-Z0-9]{14}$',
        message="ID number must be 14 characters long and contain only uppercase letters and numbers."
    )

    # Personal Information
    name = models.CharField(
        max_length=100,
        help_text=_("Full name of the staff member")
    )
    sex = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female")],
        default="male",
        help_text=_("Gender of the staff member")
    )
    date_of_birth = models.DateField(default=timezone.now,
        help_text=_("Date of birth of the staff member")
    )
    ID_number = models.CharField(
        max_length=14,
        unique=True,
        validators=[id_validator],
        help_text=_("National ID number or passport number")
    )
    email = models.EmailField(
        unique=True,
        help_text=_("Official email address")
    )
    tel_no = models.CharField(
        max_length=22,
        validators=[phone_validator],
        help_text=_("Contact phone number")
    )
    photo = models.ImageField(
        upload_to='staff_photos/',
        null=True,
        blank=True,
        help_text=_("Staff member's photograph")
    )
    address = models.TextField(default='',
        help_text=_("Physical address of residence")
    )

    # Emergency Contact
    emergency_contact_name = models.CharField(
        max_length=100, default='',
        help_text=_("Name of emergency contact person")
    )
    emergency_contact_relationship = models.CharField(
        max_length=50, default='',
        help_text=_("Relationship with emergency contact person")
    )
    emergency_contact_phone = models.CharField(
        max_length=22, default='',
        validators=[phone_validator],
        help_text=_("Emergency contact phone number")
    )

    # Employment Information
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default="teacher",
        help_text=_("Staff member's role in the school")
    )
    date_hired = models.DateField(
        auto_now_add=True,
        help_text=_("Date when staff member was hired")
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text=_("Last update timestamp")
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True, default='',
        help_text=_("School-issued employee ID")
    )

    # Qualification Information
    qualification = models.TextField( default='',
        help_text=_("Academic and professional qualifications")
    )
    certificates = models.FileField(
        upload_to='staff_certificates/',
        null=True,
        blank=True,
        help_text=_("Scanned copies of certificates")
    )
    years_of_experience = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_("Total years of professional experience")
    )

    # Teaching Staff Information
    class_name = models.CharField(
        max_length=50,
        choices=CLASS_CHOICES,
        blank=True,
        null=True,
        help_text=_("Primary class assigned to teacher")
    )
    subject_handled = models.CharField(
        max_length=50,
        choices=SUBJECT_CHOICES,
        null=True,
        blank=True,
        help_text=_("Subject taught by the teacher, only one subject allowed.")
    )

    # Non-teaching Staff Information
    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        blank=True,
        null=True,
        help_text=_("Department for non-teaching staff")
    )

    # Salary Information
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Monthly salary amount")
    )
    bank_account_name = models.CharField(
        max_length=100, default='',
        help_text=_("Name as it appears on bank account")
    )
    bank_account_number = models.CharField(
        max_length=50, default='',
        help_text=_("Bank account number for salary payment")
    )
    bank_name = models.CharField(
        max_length=100, default='',
        help_text=_("Name of the bank")
    )

    class Meta:
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff"
        ordering = ['name', 'role']

    # Properties
    @property
    def is_teaching_staff(self):
        """Check if staff member is in a teaching role"""
        return self.role in ["teacher"]

    @property
    def full_position(self):
        """Get full position description"""
        if self.is_teaching_staff:
            return f"{self.role.title()} - {self.class_name}"
        return f"{self.role.title()} - {self.department}"

    # Methods
    def clean(self):
        """Validate model data"""
        if not self.is_teaching_staff:
            if self.subject_handled is not None:
                raise ValidationError(_("Non-teaching staff cannot have subjects assigned."))
            if self.class_name:
                raise ValidationError(_("Non-teaching staff cannot be assigned to a class."))
        else:
            if not self.class_name:
                raise ValidationError(_("Teaching staff must be assigned to a class."))
            if self.subject_handled is None:
                raise ValidationError(_("Teaching staff must have a subject assigned."))
        
        if self.is_teaching_staff and self.department:
            raise ValidationError(_("Teaching staff should not be assigned to a department."))
        
        if not self.is_teaching_staff and not self.department:
            raise ValidationError(_("Non-teaching staff must be assigned to a department."))

    def save(self, *args, **kwargs):
        """Override save method to run clean()"""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_contact_info(self):
        """Return all contact information"""
        return {
            'email': self.email,
            'phone': self.tel_no,
            'address': self.address,
            'emergency_contact': {
                'name': self.emergency_contact_name,
                'relationship': self.emergency_contact_relationship,
                'phone': self.emergency_contact_phone
            }
        }

    def assign_subject(self, subject):
        """Assign a subject to teaching staff"""
        if not self.is_teaching_staff:
            raise ValidationError(_("Cannot assign subjects to non-teaching staff"))
        self.subject_handled.add(subject)

    def remove_subject(self, subject):
        """Remove a subject from teaching staff"""
        if not self.is_teaching_staff:
            raise ValidationError(_("Cannot remove subjects from non-teaching staff"))
        self.subject_handled.remove(subject)

    def __str__(self):
        """String representation of the staff member."""
        if self.is_teaching_staff:
            subject = self.subject_handled.name if self.subject_handled else 'No subject assigned'
            return f"{self.name} - {self.role} ({subject} in {self.class_name or 'No class assigned'})"
        return f"{self.name} - {self.role} ({self.department or 'No department assigned'})"

class About(models.Model):
    title = models.CharField(max_length=255, default="Our School Anthem")
    anthem = models.TextField(help_text="Write the anthem with each stanza separated by a new line.")  # Field for storing the anthem text

    def __str__(self):
        return "About Page Content"

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery_images/')  # Save images in a specific folder
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title or f"Image {self.id}"
