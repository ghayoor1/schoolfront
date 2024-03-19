from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    country=models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + "   " + self.last_name
    
def get_default_user_id():
    # Retrieve the ID of an existing user (replace 'user_id' with an actual user ID)
    return User.objects.first().id

    
class Contact(models.Model):
    username = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends_list')
    
    
    def __str__(self):
        return self.username 
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    liked_users = models.ManyToManyField(User, related_name='liked_images', blank= True)
    disliked_users = models.ManyToManyField(User, related_name='disliked_images', blank= True)

