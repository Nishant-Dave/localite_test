from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserManager(BaseUserManager):
    def create_user(self, email_id, password=None, **extra_fields):
        email_id = self.normalize_email(email_id)
        user = self.model(email_id=email_id, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_id, name, password=None, **extra_fields):
        user = self.create_user(email_id, name, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    # id_users = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    email_id = models.EmailField(unique=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # id = models.IntegerField(default=1)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'


    def __str__(self):
        return self.email_id

    def generate_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }




class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='id')

    class Meta:
        db_table = 'user_post'




class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_id = models.EmailField(default='email')
    city = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='id', default=1)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


    def __str__(self):
        return self.user.email_id
    
    class Meta:
        db_table = 'user_profile'


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='id', default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id', default=1)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'add_comment'



class FriendStatus(models.Model):
    status_choice = {
        ('N', 'None'),
        ('P', 'Pending'),
        ("F", 'Friends')
    }
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='id', default=1, related_name='sent_friend_status')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='id', default=1, related_name='received_friend_status')
    status = models.TextField(choices=status_choice)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'friend_status'



