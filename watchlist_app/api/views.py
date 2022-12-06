from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError 
from watchlist_app.models import Watchlist,StreamPlatform,Review
from watchlist_app.api.serializers import WatchlistSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework import status 
from rest_framework.views import APIView #class based views
# from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly ,IsAuthenticated
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchlistPagination,WatchListLOPagination,WatchListCPagination

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    def get_queryset(self):
        # username = self.kwargs['username'] # filtering through URL
        username = self.request.query_params.get('username') #filtering through parameter
        return Review.objects.filter(review_user__username=username)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle] 
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all() 
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = Watchlist.objects.get(pk=pk)
        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this Watchlist!")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly] 
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#----------------------------------------
#using model view set post,get,put,delete everything will be covered by default

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly] 
    
#using view set 
# class StreamPlatformVS(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)  
        
#     def create(self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save() 
#             return Response(serializer.data,status=status.HTTP_201_CREATED) 
#         else:
#             return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND) 
    
#     def update(self,request,pk=None):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except platform.DoesNotExist:
#             return Response({'Error':'StreamPlatform not found'},status=status.HTTP_404_NOT_FOUND)    
#         serializer = StreamPlatformSerializer(platform,data=request.data)
#         if serializer.is_valid():
#             serializer.save() 
#             return Response(serializer.data,status=status.HTTP_200_OK) 
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    
#     def destroy(self, request, pk=None):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response({'Error':'StreamPlatform Deleted'},status=status.HTTP_204_NO_CONTENT)


# class StreamPlatformAV(APIView):
#     def get(self,request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save() 
#             return Response(serializer.data,status=status.HTTP_201_CREATED) 
#         else:
#             return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND) 
        
# class StreamPlatformDetailsAV(APIView):
#     def get(self,request,pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except platform.DoesNotExist:
#             return Response({'Error':'StreamPlatform not found'},status=status.HTTP_404_NOT_FOUND)    
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     def put(self,request,pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except platform.DoesNotExist:
#             return Response({'Error':'StreamPlatform not found'},status=status.HTTP_404_NOT_FOUND)    
#         serializer = StreamPlatformSerializer(platform,data=request.data)
#         if serializer.is_valid():
#             serializer.save() 
#             return Response(serializer.data,status=status.HTTP_200_OK) 
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self,request,pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response({'Error':'StreamPlatform Deleted'},status=status.HTTP_204_NO_CONTENT)

class WatchListGV(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    # pagination_class = WatchlistPagination
    # pagination_class = WatchListLOPagination
    pagination_class = WatchListCPagination
    #Using filtering
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']
    #Using Search
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    #using Ordering
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields  = ['avg_rating']
    
class WatchlistAV(APIView):
    permission_classes = [IsAdminOrReadOnly] 
    def get(self,request):
        watchlist = Watchlist.objects.all()
        serializer = WatchlistSerializer(watchlist,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data,status=status.HTTP_201_CREATED) 
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND) 
        
class WatchDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly] 
    def get(self,request,pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'Error':'Watchlist not found'},status=status.HTTP_404_NOT_FOUND)    
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        try:
            watchlist = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'Error':'Watchlist not found'},status=status.HTTP_404_NOT_FOUND)    
        serializer = WatchlistSerializer(watchlist,data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data,status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        watchlist = Watchlist.objects.get(pk=pk)
        watchlist.delete()
        return Response({'Error':'Watchlist Deleted'},status=status.HTTP_204_NO_CONTENT)