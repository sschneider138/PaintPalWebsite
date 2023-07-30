from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    paintUsedGallons = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paintUsedLiters = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prevPaintUsedGallons = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prevPaintUsedLiters = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f'{self.user.username} Profile'
    
    def resetPaintUsed(self):
        self.prevPaintUsedGallons = self.paintUsedGallons
        self.prevPaintUsedLiters = self.paintUsedLiters
        self.paintUsedGallons = 0
        self.paintUsedLiters = 0
        self.save()

    def undoResetPaintUsed(self):
        self.paintUsedGallons = self.prevPaintUsedGallons
        self.paintUsedLiters = self.prevPaintUsedLiters
        self.save()

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
