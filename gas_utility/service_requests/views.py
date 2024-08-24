from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import ServiceRequest, RequestTracking
from .forms import ServiceRequestForm, SignUpForm
from django.contrib.auth.views import LogoutView, LoginView
from django.utils import timezone
from django.core.exceptions import PermissionDenied

def login(request):
    return LoginView.as_view()(request)

def logout(request):
    return LogoutView.as_view()(request)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def show_requests(request):
    if request.user.is_superuser:
        service_requests = ServiceRequest.objects.all()  # Fetch all requests for superusers
    else:
        service_requests = ServiceRequest.objects.filter(customer=request.user)  # Fetch only the logged-in user's requests

    return render(request, 'show_requests.html', {'service_requests': service_requests})

@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            print("ServiceRequest saved successfully")  # Debugging line
            return redirect('home')
        else:
            print("Form is not valid:", form.errors)  # Debugging line
    else:
        form = ServiceRequestForm()
    return render(request, 'submit_request.html', {'form': form})

@login_required
def update_service_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    # Check if the request is from the owner or admin
    if service_request.customer != request.user and not request.user.is_superuser:
        raise PermissionDenied("You are not allowed to update this request.")

    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes')

        # Update the service request status
        service_request.status = new_status
        if new_status == 'resolved':
            service_request.resolved_at = timezone.now()
        service_request.save()

        # Create a new tracking entry
        tracking = RequestTracking.objects.create(
            service_request=service_request,
            status=new_status,
            updated_by=request.user,
            notes=notes
        )
        print(f"Tracking entry created: {tracking}")  # Debugging line

        return redirect('service_request_detail', pk=service_request.pk)

    return render(request, 'service_request_update.html', {'service_request': service_request})

@login_required
def track_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    return render(request, 'track_request.html', {'service_request': service_request})


@login_required
def delete_service_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)

    # Only allow superusers to delete service requests
    # if not request.user.is_superuser:
    #     raise PermissionDenied("You are not allowed to delete this request.")

    service_request.delete()
    return HttpResponseRedirect(reverse('home'))


@login_required
def service_request_detail(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    tracking_history = service_request.trackings.all()  # Retrieve tracking entries

    return render(request, 'service_request_detail.html', {
        'service_request': service_request,
        'tracking_history': tracking_history
    })
