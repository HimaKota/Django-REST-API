from rest_framework import serializers
from watchlist_app.models import Movie

#for modelserializer we have to include validator code seperately like below
class MovieSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ['id', 'name', 'description', 'is_active','len_name']
        # exclude = ['name']
        
    #for adding custom fields
    def get_len_name(self,objects):
        length = len(objects.name)
        return length
      
        #Field-level validation
    def validate_name(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Name is too short")
        return value
    
#      # Object-level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and Description should be different")
        return data
#validator
# def name_length(value):
#     if len(value) <= 10:
#         raise serializers.ValidationError('Name is too short')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     is_active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         """
#         Create and return a new `Movie` instance, given the validated data.
#         """
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Movie` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.is_active = validated_data.get('is_active', instance.is_active)
#         instance.save()
#         return instance
    
#     adding validation methods
#     Field-level validation
#     def validate_name(self, value):
#         if len(value) < 10:
#             raise serializers.ValidationError("Name is too short")
#         return value
    
#      # Object-level validation
#      def validate(self, data):
#          if data['name'] == data['description']:
#              raise serializers.ValidationError("Name and Description should be different")
#          return data