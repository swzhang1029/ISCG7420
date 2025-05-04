from django.contrib import admin
from .models import Booking, UserProfile

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'start_time', 'room')
    search_fields = ('user__username', 'room__name', 'purpose')
    ordering = ('-start_time',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'receive_notifications')
    list_filter = ('role', 'receive_notifications')
    search_fields = ('user__username', 'phone_number')
    ordering = ('user__username',)
