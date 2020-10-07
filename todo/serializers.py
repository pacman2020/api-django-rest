from django.db.models import fields
from rest_framework import serializers
from .models import Post

class SerializePost(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','name','description')