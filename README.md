# Benedict-School
A Joint Project 
Nice! Let’s plan an appealing and appropriate web structure for a kindergarten and primary school 🌟📚.

Here’s an outline for a **child-friendly, engaging, and functional website structure**. The goal is to create a safe, warm, and inviting online presence for parents, kids, and teachers, ensuring easy navigation and visually appealing design elements.

---

### **Website Structure for Kindergarten & Primary School**

1. **Home Page**  
   _Bright, welcoming design with interactive visuals (cute animations, child-friendly icons)._  
   **Sections:**
   - **Hero Section**: A warm welcome with the school’s name, tagline (e.g., "Building Bright Futures!"), and a big colorful image of children happily learning.
   - **Call to Action**: Buttons like "Admissions", "Tour Our School", "Contact Us".
   - **Upcoming Events**: Showcase important dates (e.g., events, holidays).
   - **Short Welcome Message**: Brief intro from the principal or school philosophy.
   - **Testimonials**: Quotes from parents and students.

2. **About Us**  
   **Sections:**
   - **Our Mission & Vision**: School’s goals, values, and educational philosophy.
   - **History & Founding**: Story of the school’s founding.
   - **Team Section**: Pictures and bios of teachers and staff with friendly descriptions.
   - **Accreditation & Achievements**: Show off awards, affiliations, or certifications.

3. **Programs**  
   _Display the various programs offered (kindergarten, primary, after-school activities)._  
   **Sections:**
   - **Curriculum Overview**: Brief descriptions of kindergarten and primary-level curriculums.
   - **Special Programs**: Highlight things like art, sports, or language classes.
   - **Classroom Environment**: Pictures or videos showing a safe and nurturing environment.

4. **Admissions Page**  
   **Sections:**
   - **Admission Process**: Step-by-step guide to applying.
   - **Admission Forms**: Downloadable forms (or fill out online).
   - **Tuition & Fees**: Transparent info on fees, payment methods, and financial aid options.
   - **Schedule a Tour**: Option to book a school visit.
   
5. **Parent Resources**  
   **Sections:**
   - **School Calendar**: Important dates (e.g., holidays, events, PTA meetings).
   - **Parent Handbook**: Guidelines, policies, and FAQs.
   - **Blog/Articles**: Parenting tips, educational resources, or updates from the school.
   - **Meal Plans**: Information on school lunches and healthy snacks.

6. **Gallery/Media**  
   **Sections:**
   - **Photo Gallery**: Fun photos of children learning, playing, and celebrating.
   - **Video Tours**: Virtual tour of classrooms and facilities.
   - **Event Highlights**: Pictures from events like annual day, sports day, and festivals.

7. **Contact Us**  
   **Sections:**
   - **Contact Form**: Simple form for parents to ask questions or request info.
   - **Map & Directions**: School’s location embedded in Google Maps.
   - **Social Media Links**: Quick access to the school's Facebook, Instagram, etc.

8. **Alumni Section** (Optional but good for the future)  
   **Sections:**
   - **Success Stories**: Share stories of past students who have excelled.
   - **Stay Connected**: Option for alumni to get involved (e.g., mentorship).

---

### **Key Design Elements**  
- **Bright Colors & Child-Friendly Icons**: Soft pastels or bold primary colors paired with simple, playful icons.
- **Interactive Elements**: Hover effects, moving graphics to make it more engaging.
- **Clear Fonts & Large Text**: Ensure the text is readable, especially for parents browsing on mobile devices.
- **Inclusive Imagery**: Photos that show diversity in children and staff.
- **Mobile-Friendly**: Ensure the website is responsive on all devices.
- **Safety First**: Child protection/privacy policy clearly displayed.

from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)  # For event images
    video = models.FileField(upload_to='event_videos/', null=True, blank=True)  # For event videos

    def __str__(self):
        return self.title

class Parent(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.username

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(upload_to='child_images/', null=True, blank=True)
    application_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('left', 'Left')
    ], default='pending')

    def __str__(self):
        return self.name

class StudentApplication(models.Model):
    child = models.OneToOneField(Child, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    documents = models.FileField(upload_to='applications/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

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

