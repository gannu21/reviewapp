from django.db import models

# Create your models here.

from django.utils.timezone import now

def restaurant_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/restaurant_name/YYYYMMDD/filename
    date = now().strftime('%Y%m%d')
    restaurant_name = filename.split('_')[0]
    return 'media/{0}/{1}/{2}'.format(restaurant_name, date, filename)

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)

class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=restaurant_directory_path)
