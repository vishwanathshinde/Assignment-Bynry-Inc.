from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_request, name='submit_request'),
    path('update/<int:pk>/', views.update_service_request, name='update_service_request'),
    path('detail/<int:pk>/', views.service_request_detail, name='service_request_detail'),
    path('track/<int:request_id>/', views.track_request, name='track_request'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('show_requests/', views.show_requests, name='show_requests'),
    path('service_requests/<int:pk>/delete/', views.delete_service_request, name='delete_service_request'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)