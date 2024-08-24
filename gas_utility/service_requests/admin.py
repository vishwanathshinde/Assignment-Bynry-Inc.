# from django.contrib import admin
# from .models import ServiceRequest

# admin.site.register(ServiceRequest)

from django.contrib import admin
from .models import ServiceRequest, RequestTracking

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id','request_type', 'status', 'submitted_at', 'resolved_at', 'customer']
    list_filter = ['status', 'request_type']
    search_fields = ['description']
    # Optionally, you can add more functionality like ordering or read-only fields.

@admin.register(RequestTracking)
class RequestTrackingAdmin(admin.ModelAdmin):
    list_display = ['service_request', 'status', 'updated_at', 'updated_by', 'notes']
    list_filter = ['status', 'updated_by']
    search_fields = ['notes']
    # Optionally, you can add more functionality like ordering or read-only fields.
