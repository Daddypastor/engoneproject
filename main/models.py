from django.db import models
from ckeditor.fields import RichTextField
from django_countries.fields import CountryField
from django.contrib.auth.models import User,AbstractUser
from django.utils.html import mark_safe
from django.template.defaultfilters import slugify

# Custom User Model

class Category(models.Model):
    title= models.CharField(max_length=500, null=True)
    icon = models.CharField(max_length=500, null=True, blank=True)
    description=models.CharField(max_length=800, null=True, blank=True)

    def __str__(self):
        return self.title

status_state=(
        ('Student','Student'),
        ('Engineer','Engineer'),
        ('Senior','Senior Engineer'),
        ('Technical','Technical Engineer'),
    )

depart=(
        ('Mechone','Mechone- Mechanical Engineering'),
        ('Civilone','Civilone- Civil Engineering'),
        ('Electrone','Electrone- Electrical Engineering'),
        ('Computone','Computone- Computer Engineering'),
        ('Chemone','Chemone- Chemical Engineering'),
        ('Industrone','Industrone- Industrial Engineering')
    )
class CustomUser(AbstractUser):
    bio=RichTextField()
    profile_pic = models.ImageField(upload_to="profile/",default="pro_pic.png", null=True)
    country = CountryField(blank_label='Select Country', null=True)
    department = models.CharField(choices=depart,max_length=21, null=True)
    status = models.CharField(choices=status_state,max_length=21, null=True)
    web_link= models.URLField(null=True, blank=True)
    twi_link= models.URLField(null=True, blank=True)
    fb_link= models.URLField(null=True, blank=True)
    Ins_link= models.URLField(null=True, blank=True)
    ytube_link= models.URLField(null=True, blank=True)
    email_alert = models.BooleanField(default=False)
    questions= models.IntegerField(default=0, blank=True)
    answers= models.IntegerField(default=0, blank=True)
    reputation = models.IntegerField(default=0, blank=True)
    gold_badge = models.IntegerField(default=0, blank=True)
    silver_badge = models.IntegerField(default=0, blank=True)
    bronze_badge = models.IntegerField(default=0, blank=True)
    total_badge = models.IntegerField(default=0, blank=True)
    comment = models.IntegerField(default=0, blank=True)
    moderator = models.BooleanField(default=False)
    date_joined= models.DateTimeField(auto_now_add=True)


class Subscriber(models.Model):
    user=models.CharField(max_length=500, null=True)
    email = models.EmailField(null=True)
    add_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user

class MailMessage(models.Model):
    title = models.CharField(max_length=500, null=True)
    message = RichTextField()

    def __str__(self):
        return self.title

# Question Model
class Question(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=500)
    detail=RichTextField()
    tags=models.TextField(default='')
    category= models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="question/", default="pro_pic.png", null=True, blank=True)
    answer_alarm = models.BooleanField(default=True)
    agree_PP= models.BooleanField(default=False, blank=False)
    add_time=models.DateTimeField(auto_now_add=True)
    topic_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class QuestFollower(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='quest_user', null=True)
    quest = models.ForeignKey(Question,on_delete=models.CASCADE)
    follower= models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.quest.title


# Answer Model
class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="answer/", default="pro_pic.png",null=True, blank=True)
    detail=RichTextField()
    accepted= models.BooleanField(default=False, blank=False)
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.detail

# Comment
class Comment(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comment_user')
    comment=models.TextField(default='')
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

# UpVotes
class UpVote(models.Model):     
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='upvote_user')

# DownVotes
class DownVote(models.Model):
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='downvote_user')

class Notification(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='not_user', null=True)
    quest = models.ForeignKey(Question,on_delete=models.CASCADE)
    action_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    action =  models.CharField(max_length=21, null=True)
    is_read = models.BooleanField(default=False)
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action

class BadgeType(models.Model):
    title = models.CharField(max_length=20)
    desc = models.CharField(max_length=500, blank=True)    

    def __str__(self):
        return self.title

class Badge(models.Model):
    typename = models.ForeignKey(BadgeType, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50) 
    desc = models.CharField(max_length=500) 

    def __str__(self):
        return self.title

class Badge_Input(models.Model):
    typename = models.ForeignKey(BadgeType, on_delete=models.CASCADE, null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='bagde_user')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)  
    add_time = models.DateTimeField(auto_now_add=True, null=True)      

class Contact(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return self.name

class Faq(models.Model):
    faq = models.CharField(max_length=500)
    details = RichTextField()   

    def __str__(self):
        return self.faq