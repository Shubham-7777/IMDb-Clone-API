from django.urls import path
from watchlist_app.api.views import  UserReview,         \
                                    ReviewCreate,       \
                                    ReviewList,         \
                                    ReviewDetailAP,     \
                                    StreamPlatformAP,   \
                                    MovieListAllAV,         \
                                    MovieListAV
                                    #StreamPlatformGV,  \
                                    #MovieReviewList,    \
                                    


app_name = 'watchlist_app' 

urlpatterns = [

    path('movie-list-all/<slug:streamplaltform_slug>/', MovieListAllAV.as_view(), name='movie_list_url_streamplaltform_slug'),
    
    path('movie-list/<slug:movielist_slug>/', MovieListAV.as_view(), name='movie_list_url_movielist_slug'),
    
    path('stream-platform/<slug:slug>/', StreamPlatformAP.as_view(), name='stream-plaform'),
    
    path('reviews/', UserReview.as_view(), name='users_review_url'),
    path('reviews/<slug:slug>/', ReviewDetailAP.as_view(), name='reviews_detail_url'),
    path('<slug:slug>/',  ReviewList.as_view(), name='review_list'),
    #path('movies-list/', MovieReviewList.as_view(), name='movie_list_url'),
    path('create/<slug:slug>/', ReviewCreate.as_view(), name= 'create_review_url'),
    
    
    #path('reviews/<slug:slug>/', ReviewDetail.as_view(), name='reviews_detail_url'),
    #path('stream-platform/', StreamPlatformGV.as_view(), name='stream-plaform-list'),
    
    #StreamPlatform
     
]