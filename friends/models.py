from django.db import models

# Create your models here.
class friends(models.Model):
	uid = models.CharField(max_length=30)
	friendid = models.CharField(max_length=30)
	friendname = models.CharField(max_length=50)

class friend_req_status(models.Model):
	uid = models.CharField(max_length=30)
	friendid = models.CharField(max_length=30)
