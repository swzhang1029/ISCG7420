from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, UserProfile
from rooms.models import Room

# Create your views here.

@login_required
def create_booking(request, room_id):
    """View to create a new booking."""
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        purpose = request.POST.get('purpose')
        
        # Check for booking conflicts
        conflicting_bookings = Booking.objects.filter(
            room=room,
            status='confirmed',
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if conflicting_bookings.exists():
            messages.error(request, 'This room is already booked for the selected time slot.')
            return redirect('room_detail', room_id=room_id)
        
        booking = Booking.objects.create(
            room=room,
            user=request.user,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            created_by=request.user
        )
        messages.success(request, 'Booking created successfully!')
        return redirect('booking_detail', booking_id=booking.id)
    
    return render(request, 'bookings/create_booking.html', {'room': room})

@login_required
def booking_detail(request, booking_id):
    """View to show details of a specific booking."""
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def my_bookings(request):
    """View to list all bookings of the current user."""
    bookings = Booking.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    """View to cancel a booking."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.user != request.user and not request.user.userprofile.role == 'admin':
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('my_bookings')
    
    if booking.start_time <= timezone.now():
        messages.error(request, 'Cannot cancel past bookings.')
        return redirect('my_bookings')
    
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking cancelled successfully!')
    return redirect('my_bookings')

def register(request):
    """View to register new users."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                role='user',
                receive_notifications=True
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('rooms:room_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
