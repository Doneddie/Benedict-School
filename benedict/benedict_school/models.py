from django.db import models


class Parent(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    id_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )

    def __str__(self):
        return self.username


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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Staff-related information
    subjects_handled = models.CharField(
        max_length=100,
        choices=[
            ("math", "Mathematics"),
            ("science", "Science"),
            ("english", "English"),
            ("history", "History"),
            ("geography", "Geography"),
            ("art", "Art"),
            ("music", "Music"),
            ("physical_education", "Physical Education"),
            ("computing", "Computing"),
        ],
        default="math",
    )

    years_of_experience = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
