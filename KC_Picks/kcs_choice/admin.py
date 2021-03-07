from django.contrib import admin
from .models import ItemGroup, RatedItem, CurrentRating

# Register your models here.
admin.site.register(ItemGroup)
admin.site.register(RatedItem)
admin.site.register(CurrentRating)
