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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user_id, null=True)
    username = models.CharField(max_length=100)


    
    def __str__(self):
        return self.username 
    