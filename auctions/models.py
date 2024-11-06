from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

def get_default_user():
    return User.objects.first().id

class Listings(models.Model):
    class Meta:
        verbose_name = 'Listings'
        verbose_name_plural = 'Listings'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = get_default_user, related_name="listers")
    title = models.CharField(max_length=150)
    description = models.TextField()
    img_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    initial_bid = models.DecimalField(max_digits=10, decimal_places=2)
    closed = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} listed {self.title} at {self.initial_bid}"


class Bids(models.Model):
    
    class Meta:
        verbose_name = 'Bids'
        verbose_name_plural = 'Bids'
        
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bids')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid {self.price} on {self.listing.title}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_by')
    listing = models.ForeignKey(Listings, related_name='watchlist', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s watchlist"
    
class Comments(models.Model):
    class Meta:
        verbose_name = 'Comments'
        verbose_name_plural = 'Comments'
        
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} commented '{self.comment}' on {self.listing.title}"

class Winners(models.Model):
    class Meta:
        verbose_name = 'Winners'
        verbose_name_plural = 'Winners'
    
    listing =  models.OneToOneField(Listings, related_name="winnings", on_delete=models.CASCADE)
    user = models.OneToOneField(User, related_name="winner", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} won the bid on {self.listing.title}"