from django.db import models


class Parent(models.Model): 
    first_name = models.CharField(max_length=50, default='Unknown')
    last_name = models.CharField(max_length=50, default='Unknown') 
    ID_number = models.CharField(max_length=14, unique=True, null=False, default='AA0000000A00AA')
    email = models.EmailField(unique=True) 
    address = models.CharField(max_length=100)
    profile_image = models.ImageField(
        upload_to="parent_images/", null=True, blank=True
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Child(models.Model):
    parent = models.ForeignKey(
        Parent, on_delete=models.CASCADE, related_name="children"
    )
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
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


class Activity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title


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
    # Personal information
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    teacher_name = models.CharField(max_length=100, default='Unknown')
    class_name = models.CharField(max_length=50, default='Primary One')

    # Staff-related information
    subjects_handled = models.CharField(
        max_length=100,
        choices=[
            ("math", "Mathematics"),
            ("science", "Science"),
            ("english", "English"),
            ("social_studies", "Social Studies"),
            ("literacy_1A", "Literacy 1A"),
            ("literacy_1B", "Literacy 1B"),
            ("literacy", "Literacy"),
            ("luganda", "Luganda"),
            ("reading", "Reading"),
            ("religious_education", "Religious Education"),
            ("learning_area_1_5", "Learning Area 1-5"),
        ],
        default="math",
    )

    years_of_experience = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.teacher_name} teaches {self.subjects_handled} in {self.class_name}"


class About(models.Model):
    description = models.TextField()
    anthem = models.TextField()  # Field for storing the anthem text

    def __str__(self):
        return "About Page Content"
