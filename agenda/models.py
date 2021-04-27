from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    username = models.CharField(max_length=20,primary_key=True)
    name  = models.CharField(max_length=30)
    image = models.CharField(max_length=20,default="default.jpg")
    email = models.EmailField(null=True)
    def __str__(self):
        return self.username


class Agenda(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(Users,on_delete=models.CASCADE)
    slug = models.SlugField(default='default',editable='False',max_length=100,null=False)


    def __str__(self):
        return self.title
    
  
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value,allow_unicode=True)
        super().save(*args, **kwargs)

class Aye(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    comments = models.TextField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    @property
    def aye_count(self):
        return self.agenda.count()

    def __str__(self):
        return str(self.id)


class Nay(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    comments = models.TextField(max_length=255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)
    @property
    def nay_count(self):
        return self.agenda.count()


class UserFollowing(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='following')
    following_user = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='follower')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)