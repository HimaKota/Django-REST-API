from rest_framework import serializers
from watchlist_app.models import Watchlist,StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'        
        exclude = ('watchlist',)

#one watchlist have only one streaming platform        
class WatchlistSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source = 'platform.name')
    class Meta:
        model = Watchlist
        fields = '__all__'
        
   
#one stream platform can have multiple movies or series     
class StreamPlatformSerializer(serializers.ModelSerializer):
    #watchlist is the related name in Watchlist models platform fields
    watchlist = WatchlistSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'       