from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    def get_profile(self):
        return Profile.objects.get_or_create(user=self)[0]


class Newpost(models.Model):
    text = models.TextField()
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    date= models.DateTimeField(default=timezone.now)

    def __str__(self):
        formatted_date = self.date.strftime('%Y-%m-%d , %H:%M:%S')
        return f'{self.text} by {self.user} on {formatted_date}'
    def like_count(self):
        return Like.objects.filter(post=self).count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Newpost, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        max_length = 50  # Adjust this value as needed
        truncated_post = self.post.text[:max_length] + ("..." if len(self.post.text) > max_length else "")
        return f'{self.user.username} likes {truncated_post}'


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following')

    def __str__(self):
        return self.user.username
    
    def follower_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.user.following.count()
    


    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()