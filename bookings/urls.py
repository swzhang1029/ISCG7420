from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:room_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
] 