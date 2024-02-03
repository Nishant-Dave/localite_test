from django.urls import path
from .views import registration_view, login_view, post_view, update_profile, add_comment, send_request, accept_request, reject_request

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('post/', post_view, name='post'),
    path('update/', update_profile, name='update_profile'),
    path('add-comment/<int:post_id>/', add_comment, name='add_comment'),
    path('send-request/<int:receiver_id>/', send_request, name='send-request'),
    path('accept-request/<int:sender_id>/', accept_request, name='accept-request'),
    path('reject-request/<int:sender_id>/', reject_request, name='reject-request'),


]
