from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Beer(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="Unknown")
    beer_name = models.CharField(max_length=50)
    beer_description = models.CharField(max_length=200)
    beer_country = models.CharField(max_length=20)
    beer_label = models.CharField(max_length=20)
    beer_year = models.IntegerField(default=2000)
    beer_link = models.CharField(max_length=100, default="https://www.alko.fi")
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.beer_name
    

class Review(models.Model):
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="Unknown") #ehkä pitää olla!
    review_text = models.CharField(max_length=200, default="No review")
    stars = models.IntegerField(default=1)
    date_created = models.DateTimeField(default=timezone.now)


