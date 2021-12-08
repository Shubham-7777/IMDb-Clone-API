
from rest_framework import serializers
from watchlist_app.models import MovieList, Review, StreamPlatform, Genre
from django.contrib.auth.models import User


    
class MovieListSerializer(serializers.ModelSerializer):
    streaming_platform = serializers.CharField(source='streaming_platform.slug')
    
    class Meta:
        model = MovieList
        fields = ['title', 'slug', 'storyline', 'streaming_platform', 'active', 'avg_rating', 'number_rating', 'created']    


class ReviewSerializer(serializers.ModelSerializer):
    #review_user = serializers.StringRelatedField(source='review_user__username',read_only=True)
    #review_user = serializers.CharField(source='review_user__username', read_only=True)
    review_user = serializers.SerializerMethodField("get_username")
    
    class Meta:
        model = Review
        fields = ['review_user', 'slug', 'rating', 'description', 'reviews', 'active']    

    def get_username(self, obj):
        print(obj)
        return obj.review_user.username


class StreamPlatformSerializer(serializers.ModelSerializer):
    movie_list = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = ['name', 'about', 'website', 'movie_list']


