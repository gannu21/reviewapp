from django.shortcuts import render, redirect, get_object_or_404
from .forms import RestaurantForm, RestaurantPhotoForm
from .models import Restaurant, RestaurantPhoto
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, RestaurantPhoto
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from django.utils.timezone import now
import sys

def home(request):
    return render(request, 'journey/home.html')

#from django.shortcuts import render, redirect


def upload_photos(request):
    if request.method == 'POST':
        # Initialize an empty Restaurant instance to be populated
        restaurant_instance = None
        
        # Extract the restaurant name from the first photo's filename if available
        files = request.FILES.getlist('photo')
        if files:
            # Assuming all photos belong to the same restaurant and use the first file to extract the name
            first_file_name = files[0].name
            restaurant_name = first_file_name.split('_')[0] + '_' + now().strftime('%Y%m%d')
            
            # Create or retrieve the Restaurant instance
            restaurant_instance, created = Restaurant.objects.get_or_create(
                restaurant_name=restaurant_name,
                defaults={'comment': request.POST.get('comment', '')}
            )

        # If there's a valid Restaurant instance, save the photos
        if restaurant_instance:
            for f in files:
                photo_instance = RestaurantPhoto(restaurant=restaurant_instance, photo=f)
                photo_instance.save()

            # Assuming form data includes a comment for the restaurant
            form = RestaurantForm(request.POST, instance=restaurant_instance)
            if form.is_valid():
                # Update the restaurant instance if there's any additional info from the form
                form.save()
            return redirect('home')  # Adjust as needed
        """if request.method == 'POST':
        # Handle the restaurant form
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant_instance = form.save()
            
            # Handle the photo uploads
            files = request.FILES.getlist('photo')
            for f in files:
                photo_form = RestaurantPhotoForm(request.POST, {'photo': f})
                restaurant_name = f.name.split('_')[0] + '_' + now().strftime('%Y%m%d')
                print ("restaurant_name: ", restaurant_name, file=sys.stderr)
                # Find an existing restaurant or create a new one with the extracted name
                restaurant, created = Restaurant.objects.get_or_create(
                    restaurant_name=restaurant_name,
                    defaults={'comment': ''} # Provide defaults for other fields
                )
                if photo_form.is_valid():
                    photo_instance = photo_form.save(commit=False)
                    photo_instance.restaurant = restaurant_instance  # Link photo to the restaurant
                    photo_instance.save()
            return redirect('home')"""

    else:
        form = RestaurantForm()
        photo_form = RestaurantPhotoForm()
    return render(request, 'journey/upload_photos.html', {'form': form, 'photo_form': photo_form})

def history_comments(request):
    query = request.GET.get('q')
    if query:
        restaurants = Restaurant.objects.filter(restaurant_name__icontains=query).order_by('-date')
    else:
        restaurants = Restaurant.objects.all().order_by('-date')
    return render(request, 'journey/history_comments.html', {'restaurants': restaurants})

def your_best(request):
    return render(request, 'journey/your_best.html')

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'journey/restaurant_detail.html', {'restaurant': restaurant})

# Edit restaurant view
def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        photo_form = RestaurantPhotoForm(request.POST, request.FILES)
        if form.is_valid() and photo_form.is_valid():
            form.save()
            photo = photo_form.save(commit=False)
            photo.restaurant = restaurant
            photo.save()
            messages.success(request, 'Restaurant updated successfully!')
            return redirect('history_comments')  # Replace with the name of the URL where you list restaurants
    else:
        form = RestaurantForm(instance=restaurant)
        photo_form = RestaurantPhotoForm()
    return render(request, 'journey/edit_restaurant.html', {'form': form, 'photo_form': photo_form, 'restaurant': restaurant})

# Remove restaurant view
@require_POST
def remove_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()
    messages.success(request, 'Restaurant removed successfully!')
    return redirect('history_comments')  # Replace with the name of the URL where you list restaurants
