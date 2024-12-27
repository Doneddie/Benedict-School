from django.db import models


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
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Child(models.Model):
    parent = models.ForeignKey(
        Parent, on_delete=models.CASCADE, related_name="children"
    )
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
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
    application_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("left", "Left"),
        ],
        default="pending",
    )

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
    
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Staff(models.Model):
    # Personal information
    name = models.CharField(max_length=50, unique=True)
    ID_number = models.CharField(max_length=14, unique=True, null=False, default='')
    email = models.EmailField(unique=True)
    tel_no = models.CharField(max_length=22, default='')

    # Role/Position (New field to differentiate staff types)
    role = models.CharField(
        max_length=50,
        choices=[
            ("teacher", "Teacher"),
            ("director", "Director"),
            ("cleaner", "Cleaner"),
            ("cook", "Cook"),
            ("admin", "Admin Staff"),
            ("other", "Other")
        ],
        default="teacher"
    )

    # Teaching staff-related information (Visible only if role is "teacher")
    class_name = models.CharField(max_length=50, default='Primary One', blank=True, null=True)
    subjects_handled = models.ManyToManyField(Subject, blank=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)

    # Non-teaching staff-related information (Visible for non-teachers)
    department = models.CharField(max_length=100, blank=True, null=True)
    work_schedule = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.role == "teacher":
            return f"{self.name} teaches {self.subjects_handled} in {self.class_name}"
        else:
            return f"{self.name} works as a {self.role} in the {self.department} department"

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
