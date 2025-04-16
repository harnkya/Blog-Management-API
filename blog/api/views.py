from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsOwner
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.permissions import AllowAny
from ..models import Blog, Comment


# galiba login ve register kullanılmayacak
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  # register'a herkes erişmeli

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)

        # Kullanıcı oluşturulduktan sonra ona JWT token verelim
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class ProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # postmanda token gönderilirken "" içine alınmayacak

    def get(self, request):
        if request.user.is_authenticated:
            blogs = Blog.objects.filter(author=request.user)  # queryset
            blogs_serialized = BlogSerializer(blogs, many=True).data
            return Response({
                "username": request.user.username,
                "email": request.user.email,
                "blogs": blogs_serialized,
            }, status=status.HTTP_200_OK)

    def put(self, request):
        if request.user.is_authenticated:
            self.check_object_permissions(request, self)
            username = request.data.get("username")
            email = request.data.get("email")

            if username:
                request.user.username = username
            if email:
                request.user.email = email
            request.user.save()

            return Response({
                "username": request.user.username,
                "email": request.user.email,
            }, status=status.HTTP_200_OK)
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


class BlogsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = Blog.objects.filter(author=request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, id=None):  # takes id as a keyword argument!!!
        if id:
            try:
                blog = Blog.objects.get(id=id)
                serializer = BlogSerializer(blog)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Blog.DoesNotExist:
                return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Blog ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if id:
            try:
                blog = Blog.objects.get(id=id)
                self.check_object_permissions(request, blog)
                serializer = BlogSerializer(blog, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Blog.DoesNotExist:
                return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        if id:
            try:
                blog = Blog.objects.get(id=id)
                self.check_object_permissions(request, blog)
                blog.delete()
                return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except Blog.DoesNotExist:
                return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Blog ID is required"}, status=status.HTTP_400_BAD_REQUEST)


class CommentsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, blog_id):
        if blog_id:
            try:
                # try'a giriyor
                blog = Blog.objects.get(id=blog_id)
                print("buraya geliyor")
                comments = Comment.objects.filter(blog=blog)
                serializer = CommentSerializer(comments, many=True)  # ALWAYS USE FILTER() + MANY = TRUE
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Comment.DoesNotExist:
                return Response({"error": "Comments not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Blog ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, blog_id=None):
        if blog_id:
            try:
                blog = Blog.objects.get(id=blog_id)
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(blog=blog, author=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Blog.DoesNotExist:
                return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Blog ID is required"}, status=status.HTTP_400_BAD_REQUEST)


class CommentAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, id=None):
        if id:
            try:
                comment = Comment.objects.get(id=id)
                serializer = CommentSerializer(comment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Comment.DoesNotExist:
                return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Comment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if id:
            try:
                comment = Comment.objects.get(id=id)
                self.check_object_permissions(request, comment)  # Returns None
                serializer = CommentSerializer(comment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Comment.DoesNotExist:
                return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        if id:
            try:
                comment = Comment.objects.get(id=id)
                self.check_object_permissions(request, comment)
                comment.delete()
                return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except Comment.DoesNotExist:
                return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Comment ID is required"}, status=status.HTTP_400_BAD_REQUEST)
