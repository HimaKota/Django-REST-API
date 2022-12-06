from django.urls import path ,include
from rest_framework.routers import DefaultRouter
# from . import views
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (ReviewList,ReviewDetail,ReviewCreate,
                                     WatchlistAV,WatchDetailsAV,StreamPlatformVS,UserReview,
                                     WatchListGV)
router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/',WatchlistAV.as_view(),name='movie-list'),
    path('<int:pk>/',WatchDetailsAV.as_view(),name='movie-detail'),
    path('list2/', WatchListGV.as_view(), name='watch-list'),
    path('',include(router.urls)),
    # path('stream/',StreamPlatformAV.as_view(),name='Stream List'), 
    # path('stream/<int:pk>/',StreamPlatformDetailsAV.as_view(),name='Stream Details'), 
    # path('review/',ReviewList.as_view(),name='Review List'),
    # path('review/<int:pk>/',ReviewDetail.as_view(),name='Review Details'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),   
    path('<int:pk>/reviews/',ReviewList.as_view(),name='review-list'), 
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    # path('reviews/<str:usernamre>/',UserReview.as_view(),name='Review User Details'), #filtering through URL   
    path('user-reviews/',UserReview.as_view(),name='user-review-detail'), #filtering through parameter
]
