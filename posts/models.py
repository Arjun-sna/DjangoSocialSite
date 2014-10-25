from django.db import models

# Create your models here.
class userposts(models.Model):
	uid = models.CharField(max_length=30)
	postedby = models.CharField(max_length=50)
	post = models.CharField(max_length=300)
	post_date = models.DateTimeField(auto_now=True)


