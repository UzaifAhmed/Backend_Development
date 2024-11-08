from post_app import models
from post_app.api.serializers import PostSerializer, ProfileSerializer, CommentSerializer
from post_app.api.permissions import IsOwnerOrReadOnly, IsAuthenticatedForPostOnly

from rest_framework import generics,  response, status, filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

class PostPagination(PageNumberPagination):
    page_size = 2

class PostView(generics.ListCreateAPIView): 
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'post_user__user__username', 'comments__text__icontains']
    ordering_fields = ['created', 'likes']

    def perform_create(self, serializer):
        try:
            # Assign the post_user field to the current user's profile
            profile = self.request.user.profile
            serializer.save(post_user=profile)
            return serializer.data
        except:
            raise ValidationError({"detail": "Authentication credentials were not provided."})
        
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    # def get_queryset(self,  serializer_data):
    #     posts = models.Post.objects.get(pk=self.request.pk)
    #     if posts.DoesNotExist:
    #         raise ValidationError('Post model has no pk.')
    #     return serializer_data
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()
        return serializer.data

    # def get(self, request, pk):
    #     try:
    #         posts = models.Post.objects.get(pk=pk)
    #     except posts.DoesNotExist:
    #         return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = PostSerializer(posts)
    #     return Response(serializer.data)
    
    def perform_destroy(self, instance):
        # Get the current user and the pk values from the request path
        curr_user = self.request.user.username
        post_by = PostSerializer(instance).data.get('post_by')
        print(type(curr_user))
        print(type(post_by))

        print(curr_user)
        print(post_by)
        if curr_user == post_by:
            return super().perform_destroy(instance)
        raise ValidationError({"detail": "You are not authorized to delete this post."})
    
class PostComments(APIView):
    serializer_class = CommentSerializer

    def get(self, request, pk):
        # Get the post with the specified ID
        post = get_object_or_404(models.Post, pk=pk)

        # Retrieve all comments related to this post
        comments = models.Comments.objects.filter(post=post)
        
        # Serialize the comments queryset
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        if request.user.is_authenticated:
            # Get the post with the specified ID to associate it with the new comment
            post = get_object_or_404(models.Post, pk=pk)

            # Pass post ID in the request data for validation
            data = request.data.copy()
            data['post'] = post.id
            
            # serialize and save new comment
            serializer = CommentSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assign the post_user field to the current user's profile
        profile = self.request.user.profile
        serializer.save(post_user=profile)
        return serializer.data
    

class LikePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(models.Post, pk=pk)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            message = "Post unliked"
        else:
            post.likes.add(user)
            message = "Post liked"
        
        return Response({'message': message, 'like_count': post.likes.count()}, status=status.HTTP_200_OK)
    

class CommentCreate(APIView):
    # serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]
    queryset = models.Comments.objects.all()

    def get(self, serializer):
        posts = models.Comments.objects.all()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class CommentCreate(generics.CreateAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         # Assign the post_user field to the current user's profile
#         comment = self.request.user.profile
#         serializer.save(post_user=profile)
#         return serializer.data
# class CommentCreate(generics.CreateAPIView):
#     queryset = models.Comments.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         # Automatically assign the comment_user to the current logged-in user
#         serializer.save(comment_user=self.request.user.profile)
    

class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return models.Profile.objects.all()
    
class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return models.Profile.objects.all()
    
    def perform_update(self, serializer):
        serializer.save()
        return serializer.data
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class ProfileCreate(generics.CreateAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        # data = self.request.data
        # # print(data)
        # username = data.get('username')
        # # print(username)
        # email = data.get('email')
        # # print(email)
        # password = data.get('password')
        # # print(password)

        # if not (username and email and password):
        #     raise ValidationError("Username, email, password are required.")
        
        # if User.objects.filter(username=username).exists():
        #     raise ValidationError("Profile with this username already exists.")
        
        # user = User.objects.create_user(username=username, email=email, password=password)
        # Saving new user with bio
        serializer.save()
        
    
class ProfileUpdate(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = models.Profile.objects.all()

    def get_object(self):
        # Fetch profile by user ID from the URL parameter or by using another identifier
        user_id = self.kwargs.get('id')
        return get_object_or_404(models.Profile, user_id=user_id)
    

# class FollowProfile(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         profile = get_object_or_404(models.Profile, pk=pk)

#         print('profile belongs to ', profile)
#         # print(type(profile))
#         user_profile = request.user.profile
#         print(user_profile)
#         print('People already following ',user_profile.following.all())

#         if profile in user_profile.following.all():
#             user_profile.following.remove(profile)
#             message = "Profile Unfollowed"
#         else:
#             user_profile.following.add(profile)
#             message = "Profile Followed"

#         profile_data = ProfileSerializer(profile).data
#         user_profile_data = ProfileSerializer(user_profile).data
        
#         return Response({'message': message,
#                          'profile of': profile_data,
#                          'following_count': user_profile.following.count(),
#                          'followers_count': profile.followers.count()}, 
#                          status=status.HTTP_200_OK)


class FollowProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Retrieve the target profile that is being followed/unfollowed
        profile = get_object_or_404(models.Profile, pk=pk)
        # Get the current user's profile instance
        user_profile = request.user.profile

        # Check if the user is already following the target profile
        if profile in user_profile.following.all():
            user_profile.following.remove(profile)
            message = "Profile unfollowed"
        else:
            user_profile.following.add(profile)
            message = "Profile followed"
        
        # Return the message and updated follower count
        return Response({
            'message': message,
            'like_count': profile.followers.count()
        }, status=status.HTTP_200_OK)
    

# class FollowingFollowers(generics.ListAPIView):
#     serializer_class = ProfileSerializer
    
#     def get_queryset(self):
#         profile = get_object_or_404(models.Profile, pk=self.kwargs['pk'])
#         print(profile.followers.all(), profile.following.all(), sep="\n\n")
#         # output = {'Followers': profile.followers.all(),
#         #           'Following': profile.following.all()}
#         output = {'Followers': list(profile.values('followers', 'following'))}
#         return output
class FollowingFollowers(APIView):
    def get(self, request, pk):
        profile = models.Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(profile)


        output = {
            "followers": serializer.data['followers'],
            "following": serializer.data['following']
        }
        return Response(output)
    
    

class CommentView(generics.ListAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return models.Comments.objects.all()
    

class CommentDetail(APIView):
    serializer_class = CommentSerializer

    def get(self, request, pk, c_pk):
        try:
            comment = models.Comments.objects.get(pk=c_pk)
            if comment.post.id == pk:
                serializer = CommentSerializer(comment)
                return Response(serializer.data)
            return Response({'error': 'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)
            
        except models.Comments.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
    def delete(self, request, pk, c_pk):
        try:
            curr_user = self.request.user.profile
            # Retrieve the comment based on c_pk
            comment = models.Comments.objects.get(pk=c_pk)
            comt_by = CommentSerializer(comment)['comment_by'].value
            # Check if the comment belongs to the post with primary key pk
            if comment.post.id == pk  and curr_user == comt_by:
                comment.delete()
                return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Not the Owner Or No such Comment found'}, status=status.HTTP_400_BAD_REQUEST)
            
        except models.Comments.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
    def put(self, request, pk, c_pk):
        try:
            curr_user = self.request.user.profile
            comment = models.Comments.objects.get(pk=c_pk)
            comt_by = CommentSerializer(comment)['comment_by'].value
            if comment.post.id == pk and curr_user == comt_by:  # Ensure the comment belongs to the specified post
                serializer = CommentSerializer(comment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'No such Comment found OR you can\'t update'}, status=status.HTTP_400_BAD_REQUEST)
            
        except models.Comments.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        

class LogOut_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)