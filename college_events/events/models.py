from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)  
    description = models.TextField()        
    date = models.DateField()                
    time = models.TimeField(null=True, blank=True)               
    venue = models.CharField(max_length=255) 
    capacity = models.PositiveIntegerField()
    department = models.CharField(max_length=100) 
    eligibility = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.department = self.department.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Link to Event
    name = models.CharField(max_length=100)                     # Student's name
    email = models.EmailField()                                 # Student's email
    phone = models.CharField(max_length=15)                    # Student's phone number
    department = models.CharField(max_length=100)              # Student's department (e.g., CSE, ECE)
    year = models.PositiveSmallIntegerField()                  # Year of study (e.g., 1, 2, 3, 4)
    section = models.CharField(max_length=10)                  # Section (e.g., A, B, C)
    registration_number = models.CharField(max_length=15)      # Unique registration number
    registered_at = models.DateTimeField(auto_now_add=True)     # Timestamp of registration

    def __str__(self):
        return f"{self.name} ({self.registration_number}) - {self.event.name}"
