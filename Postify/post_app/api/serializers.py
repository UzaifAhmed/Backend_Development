from post_app.models import Post, Comments, Profile
from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(source='comment_user.user.username', read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)

    class Meta:
        model = Comments
        # fields = '__all__'
        exclude = ("comment_user",)

    def create(self, validated_data):
        # retrieve post from validated_data and  remove it
        post = validated_data.pop('post')
        validated_data['comment_user'] = self.context['request'].user.profile

        return Comments.objects.create(post=post, **validated_data)


class PostSerializer(serializers.ModelSerializer):
    post_by = serializers.CharField(source='post_user.user.username', read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_by', 'like_count', 'comments']
        # exclude = ("post_user",)

    def get_comments(self, obj):
        # Retrieve all comments where the post field matches the current post's ID
        comments = Comments.objects.filter(post=obj)
        return CommentSerializer(comments, many=True).data
    
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     print(user)
    #     return Post.objects.create(post_user_id=user.id, **validated_data)
    
    def create_comments(self, validated_data):
        # Get the logged-in user from context and assign it to comment_user
        validated_data['comment_user'] = self.context['request'].user.profile
        return super().create(**validated_data)
    


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    name = serializers.CharField(source='user.username', read_only=True)
    user_email =  serializers.CharField(source='user.email', read_only=True)
    followers = serializers.SlugRelatedField(slug_field='user__username', many=True, read_only=True)
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following = serializers.SlugRelatedField(slug_field='user__username', many=True, read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    
    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ('user',)

    def validate(self, data):
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({'error': 'This Username already exists'})
        return data

    def create(self, validated_data):

        u = validated_data.pop('username')
        e = validated_data.pop('email')
        p = validated_data.pop('password') # eniu344g493gjo3b
        # Get user from the context (request)
        user = User.objects.create_user(username=u, email=e, password=p)
        
        # Now create profile
        profile = Profile.objects.create(user=user, **validated_data)
        return profile