from django.contrib import admin
from watchlist_app.models import Review, MovieList, StreamPlatform, Genre

# Register your models here.

admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(MovieList)
admin.site.register(StreamPlatform)

