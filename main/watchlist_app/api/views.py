from django.core.exceptions import ValidationError
from watchlist_app.models import StreamPlatform, Genre, MovieList, Review
from rest_framework.response import Response

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from  watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework import permissions

from watchlist_app.models import Review
from watchlist_app.api.serializers import MovieListSerializer, ReviewSerializer, StreamPlatformSerializer



class MovieReviewList(generics.ListAPIView):
    serializer_class = MovieListSerializer
    permission_classes = [IsAuthenticated]
    queryset = MovieList.objects.all()
    
    def get_queryset(self):
        print('Movie review')
        return MovieList.objects.all()    


class UserReview(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'reviews__slug']

    def get_queryset(self):
        print(self.request.user)
        return Review.objects.all()
        #return Review.objects.filter(review_user__username=self.request.user)



class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  
    queryset = Review.objects.all()
    throttle_classes = [ReviewCreateThrottle]

    
    def get_queryset(self):
        return self.queryset


    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        movie = MovieList.objects.get(slug=slug)
        print(movie)    
        review_user = self.request.user
        review_queryset = Review.objects.filter(reviews=movie, review_user=review_user)
        print(review_queryset)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']  
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
            
        movie.number_rating += 1
        movie.save()
        
        serializer.save(reviews=movie, review_user=review_user)
        
        
class ReviewList(generics.ListAPIView):
    queryset = Review
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly, IsReviewUserOrReadOnly]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    
    def get_queryset(self):
        print('Review_List')
        slug = self.kwargs['slug']
        queryset = Review.objects.filter(reviews__slug=slug)
        return queryset
        
    
"""
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    lookup_field = 'slug'
    #throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    #throttle_scope = 'review-detail'
"""



class ReviewDetailAP(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    #renderer_classes = (TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer, )

    def get(self, request, slug):
        slug = self.kwargs['slug']
        print(slug, 'get function')
        obj = Review.objects.filter(slug=slug)
        serializer = ReviewSerializer(obj, many=True)
        return Response(serializer.data)


    def put(self, request, slug):
        slug = self.kwargs['slug']
        print(slug, 'put function')
        obj = Review.objects.get(slug=slug)
        print(request.data)
        serializer = ReviewSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('valid')
            print(serializer.data)
            return Response(serializer.data)
        else:
            print(serializer.errors)
            print('Invalid')
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, slug):
        slug = self.kwargs['slug']
        print(slug, 'delete function')
        obj = Review.objects.get(slug=slug)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            print("Obj doesn't exist")
            
"""
class StreamPlatformGV(generics.ListAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly] #IsAuthenticated
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']
"""    
                
class StreamPlatformAP(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    #throttle_classes = []
    
    def get(self, request, slug):
        print("get functionn StreamPlatform")
        slug = self.kwargs['slug']
        print(slug)
        test = "testing"
        try:
            obj = StreamPlatform.objects.get(slug=slug)
        except:
            return Response({'error': 'Stream Platform not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(obj, context = {'request': request, "test":test})
        return Response(serializer.data)
        #print(serializer.initial_data)
    
    def put(self, request, slug):
        slug = self.kwargs['slug']
        print('put request, StreamPlatform')
        print(request.data, "request.data")
        try:
            obj = StreamPlatform.objects.get(slug=slug)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Stream Platform not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)    
        
    def delete(self, request, slug):
        slug = self.kwargs['slug']
        try:
            obj = StreamPlatform.objects.get(slug=slug)
            if obj.is_exists():
                obj.delete()
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'StreamPlatform object not found or already been deleted'}, status=status.HTTP_404_NOT_FOUND)

            
            
class MovieListGV(generics.ListAPIView):
    pass


class MovieListAllAV(APIView):
    
    def get(self, request, streamplaltform_slug):
        slug = self.kwargs['streamplaltform_slug']
        print(slug)
        print('MovieListAllAV get function')
        try:
            obj = MovieList.objects.filter(streaming_platform__slug=streamplaltform_slug)
            serializer = MovieListSerializer(obj, many=True)
            return Response(serializer.data)
        except MovieList.DoesNotExist:
            return Response(serializer.errors)
    
    
    def put(self, request, streamplaltform_slug):
        slug = self.kwargs['streamplaltform_slug']
        obj = MovieList.objects.filter(streaming_platform__slug=streamplaltform_slug)
        serializer = MovieListSerializer(obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.save)
        else:
            return Response(serializer.errors)
            
    
    def delete(self, request, streamplaltform_slug):
        streamplaltform_slug = self.kwargs['slug']
        obj = MovieList.objects.get(streaming_platform__slug=streamplaltform_slug)
        if obj.is_exists():
            obj.delete()
        else:
            print('Obj already deleted or does not exist')
            
            
            
class MovieListAV(APIView):
    
    def get(self, request, movielist_slug):
        movielist_slug = self.kwargs['movielist_slug']
        print(movielist_slug)
        print('MovieListAV get function')
        try:
            obj = MovieList.objects.filter(slug=movielist_slug)
            serializer = MovieListSerializer(obj, many=True)
            return Response(serializer.data)
        except MovieList.DoesNotExist:
            return Response(serializer.errors)
    
    
    def put(self, request, streamplaltform_slug):
        movielist_slug = self.kwargs['movielist_slug']
        obj = MovieList.objects.filter(slug=movielist_slug)
        serializer = MovieListSerializer(obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.save)
        else:
            return Response(serializer.errors)
            
    
    def delete(self, request, streamplaltform_slug):
        movielist_slug = self.kwargs['movielist_slug']
        obj = MovieList.objects.get(slug=movielist_slug)
        if obj.is_exists():
            obj.delete()
        else:
            print('Obj already deleted or does not exist')
            
            
            