from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    name  = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    registeredAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Agenda(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(Users,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Aye(models.Model):
    agenda = models.ForeignKey(Agenda,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    registeredAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)


class Nay(models.Model):
    agenda = models.ForeignKey(Agenda,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    registeredAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)