from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import UserSerializer, PostSerializer, UserProfileSerializer, CommentSerializer, FriendStatusSerializer
from .models import CustomUser, Post, UserProfile, Comment, FriendStatus
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


# ----------------------- REGISTRATION VIEW ----------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ------------------------------- LOGIN VIEW ------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email_id')
        password = request.data.get('password')

        # if email is None or password is None:
        #     return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email_id=email, password=password)

        if user:
            tokens = user.generate_tokens()
            user=user.id
            return Response({'user_id': user, 'tokens': tokens}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




# -------------------------------- USER POST VIEW -------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_view(request):
    if request.method == 'POST':
        # Extract 'content' from request data
        content = request.data.get('content')

        # Set 'user' to the id of the logged-in user
        user_id = request.user.id
        print(request.user.id)
        # Create dictionary with 'content' and 'user'
        post_data = {'content': content, 'user': user_id}

        # Create serializer instance with the post data
        serializer = PostSerializer(data=post_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# -------------------------------------- UPDATE PROFILE VIEW ------------------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    if request.method == 'PUT':
        email = request.user.email_id
        fname = request.data.get('first_name')
        lname = request.data.get('last_name')
        city = request.data.get('city')
        bio = request.data.get('bio')
        
        profile_data = {'email_id': email, 'first_name': fname, 'last_name': lname, 'city': city, 'bio': bio}

        serializer = UserProfileSerializer(data=profile_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# ------------------------ ADD COMMENT CODE ------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, post_id):
    try:
        user_id = request.user.id
        # post_id = Post.objects.get(id=post_id)
        content = request.data.get('comment_text')
        print(post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    

    comment_data = {'user': user_id, 'post': post_id, 'comment_text': content}
    serializer = CommentSerializer(data=comment_data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



# ------------------------------------- FRIEND STATUS -----------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_request(request, receiver_id):
    receiver = get_object_or_404(CustomUser, id=receiver_id)

    if receiver == request.user:
        return Response({'error': 'You cannot send a friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    if FriendStatus.objects.filter(sender=request.user, receiver=receiver).exists():
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
    
    friend_request = FriendStatus.objects.create(sender=request.user, receiver=receiver, status='Pending')
    return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request, sender_id):
    # print("Sender ID:", sender_id)  
    # print("Receiver ID:", request.user.id) 
    # print(request.user)

    friend_request = get_object_or_404(FriendStatus, sender=sender_id, receiver=request.user, status='Pending')
    
    friend_request.status = 'Friends'
    friend_request.save()
    
    return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_request(request, sender_id):

    # print("Sender ID:", sender_id)  
    # print("Receiver ID:", request.user.id) 

    friend_request = get_object_or_404(FriendStatus, sender=sender_id, receiver=request.user, status='Pending')

    friend_request.delete()
    return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)
