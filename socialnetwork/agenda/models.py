from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    username = models.CharField(max_length=20,primary_key=True)
    name  = models.CharField(max_length=30)
    image = models.CharField(max_length=10,default="default.jpg")
    email = models.EmailField(null=True)
    def __str__(self):
        return self.username


class Agenda(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(Users,on_delete=models.CASCADE)
    ayes = models.ManyToManyField(Users,related_name='agenda_aye')
    nays = models.ManyToManyField(Users,related_name='agenda_nay')
    slug = models.SlugField(default='default',editable='False',max_length=100,null=False)


    def __str__(self):
        return self.title

  
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value,allow_unicode=True)
        super().save(*args, **kwargs)