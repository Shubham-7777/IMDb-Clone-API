from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Genre(models.Model):
    
    genre_choices = (("Action", "ACTION"),
            ("Adventure", "Adventure"),
            ("Comedy", "COMEDY"),
            ("Documentary", "DOCUMENTARY"),
            ("Drama", "DRAMA"),
            ("Horror", "HORROR"),
            ("Sci-Fi", "SCI_FI"),
            ("Thriller", "THRILLER"),
            ("Fantasy", "FANTASY"),
            ("Fiction", "FICTION"),
            ("Other", "OTHER"),
            )
    genre = models.CharField(choices=genre_choices, default="Other", unique=True, max_length=100)
        
    def __str__(self):
        return str(self.genre)
    
    
class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, null=False, blank=False)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=200)       
    
    def __str__(self):
        return self.name
    

class MovieList(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, default='movielist_slug')
    storyline = models.CharField(max_length=200)
    genre_type= models.ManyToManyField(Genre, related_name='genre_type_field')
    streaming_platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='stream_platform_field')
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
    
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default='review_slug')
    rating = models.PositiveIntegerField()
    description = models.CharField(max_length=200, null=True, blank=True)
    reviews = models.ForeignKey(MovieList, on_delete=models.CASCADE, related_name="reviews_field")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return str(self.rating) + " | " + self.reviews.title + " | " + str(self.review_user)
    

