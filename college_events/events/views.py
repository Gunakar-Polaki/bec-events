from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event, Registration
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import openpyxl 
from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    return render(request, 'home.html')

# User registration view
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('event_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# User login view
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)  # Log in the user
                return redirect('event_list')  # Redirect to home or another page
            else:
                form.add_error(None, 'Invalid username or password.')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home') 


# Display all events
def event_list(request):
    query = request.GET.get('search', '')  # Get the search query for event name
    department = request.GET.get('department', '')  # Get the department filter

    # Start with all events
    events = Event.objects.all()

    # Apply filter by event name (partial match using icontains)
    if query:
        events = events.filter(name__icontains=query)

    # Apply filter by department
    if department:
        events = events.filter(department__icontains=department)

    # Order events by creation date in descending order
    events = events.order_by('-created_at')

    return render(request, '../templates/events/event_list.html', {'events': events, 'query': query, 'department': department})


def event_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check eligibility (implement your logic here)
            department = form.cleaned_data['department']
            year = form.cleaned_data['year']

            if event.eligibility and department not in event.eligibility:
                return render(request, 'events/event_register.html', {
                    'form': form,
                    'event': event,
                    'alert_message': "You are not eligible to register for this event.",
                    'alert_type': "error"
                })

            # Check if already registered
            registration_number = form.cleaned_data['registration_number']
            if Registration.objects.filter(event=event, registration_number=registration_number).exists():
                return render(request, 'events/event_register.html', {
                    'form': form,
                    'event': event,
                    'alert_message': "You are already registered for this event.",
                    'alert_type': "error"
                })


            # Save the registration
            registration = form.save(commit=False)
            registration.event = event
            registration.save()

            
            return render(request, 'events/registration_email.html', {
                'registration': registration,
                'event': event
            })
    else:
        form = RegistrationForm()
    return render(request, 'events/event_register.html', {'form': form, 'event': event})


def download_data(request):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        
        # Query the selected event and registrations
        selected_event = Event.objects.get(id=event_id)
        registrations = Registration.objects.filter(event=selected_event)
        
        # Create Excel file
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = f"Registrations - {selected_event.name}"
        
        # Add headers
        headers = ['Student Name','Registration Number', 'Email', 'Phone','Department','Year','Section', 'Registration Date ad Time']
        worksheet.append(headers)
        
        # Add data rows
        for registration in registrations:
            worksheet.append([
                registration.name,
                registration.registration_number,
                registration.email,
                registration.phone,
                registration.department,
                registration.year,
                registration.section,
                registration.registered_at.strftime('%Y-%m-%d - %H:%M'),
            ])
        
        # Set response for download
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{selected_event.name}_registrations.xlsx"'
        workbook.save(response)
        
        return response

    # Fetch all events for the dropdown
    events = Event.objects.all()
    return render(request, 'events/download_data.html', {'events': events})


def addevent(request):
    if request.method == "POST":
        # Collect form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        capacity = request.POST.get('capacity')
        department = request.POST.get('department')
        eligibility = request.POST.get('eligibility')

        # Save the event
        Event.objects.create(
            name=name,
            description=description,
            date=date,
            time=time,
            venue=venue,
            capacity=capacity,
            department=department,
            eligibility=eligibility,
        )
        messages.success(request, "Event added successfully!")
        return redirect('addevent')

    return render(request, 'events/add_event.html')


@login_required
@user_passes_test(lambda u: u.is_staff)  # Ensure the user is an admin/staff
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_name = event.name
    event.delete()
    return redirect('event_list')  