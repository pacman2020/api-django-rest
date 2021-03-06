from .models import Post
from .serializers import SerializePost
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication


class PostView(APIView):
    def get(self, request, format=None):
        snippets = Post.objects.all()
        serializer = SerializePost(snippets, many=True)
        return Response(serializer.data)

class PostGet(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SerializePost(snippet)
        return Response(serializer.data)

class PostNew(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        serializer = SerializePost(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostViewDetail(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SerializePost(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
