from django.db import models

# Create your models here.
AUTHORITY = [
    (0,'normal'),
    (1,'admin')
]

class Creator(models.Model):
    user_id = models.CharField(max_length=20)
    # user_name = models.CharField(max_length=20)
    user_authority = models.IntegerField(choices=AUTHORITY,default=0)