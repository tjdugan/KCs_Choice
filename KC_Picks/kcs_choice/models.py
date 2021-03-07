from django.db import models

# Create your models here.
class ItemGroup(models.Model):
    groupTitle = models.CharField(max_length=255)
    groupDescrip = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.groupTitle)

class RatedItem(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(blank=True)
    itemGroup = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    datafield_1 = models.CharField(max_length=255, blank=True)
    datafield_2 = models.CharField(max_length=255, blank=True)
    datafield_3 = models.CharField(max_length=255, blank=True)
    datafield_4 = models.CharField(max_length=255, blank=True)
    datafield_5 = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.title)

class CurrentRating(models.Model):
    ratingOrder = models.TextField()
    itemGroup = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)

