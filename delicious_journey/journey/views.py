from django.shortcuts import render, redirect, get_object_or_404
from .forms import RestaurantForm, RestaurantPhotoForm
from .models import Restaurant, RestaurantPhoto

def home(request):
    return render(request, 'journey/home.html')

#from django.shortcuts import render, redirect


def upload_photos(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        files = request.FILES.getlist('photo') # Get the list of files
        if form.is_valid():
            restaurant_instance = form.save()
            for f in files:
                # Extract restaurant name from the file name
                restaurant_name = f.name.split('_')[0]
                
                # Find an existing restaurant or create a new one with the extracted name
                restaurant, created = Restaurant.objects.get_or_create(
                    restaurant_name=restaurant_name,
                    defaults={'comment': ''} # Provide defaults for other fields
                )
                
                # Now create a photo instance linked to the found/created restaurant
                photo_instance = RestaurantPhoto(photo=f, restaurant=restaurant)
                photo_instance.save()
            return redirect('home')
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



