from django import forms
from .models import Restaurant, RestaurantPhoto

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['comment']

class RestaurantPhotoForm(forms.ModelForm):
    class Meta:
        model = RestaurantPhoto
        fields = ['photo']
    photo = forms.ImageField(label='Select a file', required=False, widget=forms.FileInput(attrs={'multiple': True}))
