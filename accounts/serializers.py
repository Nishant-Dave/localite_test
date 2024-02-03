from rest_framework import serializers
from accounts.models import CustomUser, Post, UserProfile, Comment, FriendStatus

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('name', 'email_id', 'password')

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            name=validated_data.get('name'),
            email_id=validated_data.get('email_id'),
            password=validated_data.get('password')
        )

        # user.save()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'user']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name','bio', 'city', 'user', 'email_id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'post', 'comment_text']


class FriendStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendStatus
        fields = ['sender', 'receiver', 'status']