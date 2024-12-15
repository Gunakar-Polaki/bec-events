from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue', 'capacity', 'department','eligibility')  # Fields to display in the list view
    search_fields = ('name', 'venue', 'department','eligibility') 
    list_filter = ('department','date')                  


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'email', 
        'phone', 
        'department', 
        'year', 
        'section', 
        'registration_number', 
        'event', 
        'registered_at'
    )  # Fields to display in the list view

    search_fields = (
        'name', 
        'email', 
        'registration_number', 
        'department'
    )  # Fields to search by

    list_filter = ('event', 'year', 'department')  # Fields to filter by
