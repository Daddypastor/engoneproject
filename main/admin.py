from django.contrib import admin
from .models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display=('title','user','category','answer_alarm','agree_PP')
    search_fields=('title','detail')
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(QuestFollower)
admin.site.register(Notification)
admin.site.register(Subscriber)
admin.site.register(MailMessage)

class CommentAdmin(admin.ModelAdmin):
    list_display=('answer','comment')
admin.site.register(Comment,CommentAdmin)

class UpvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')
admin.site.register(UpVote,UpvoteAdmin)

class DownvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')
admin.site.register(DownVote,DownvoteAdmin)

class BadgeAdmin(admin.ModelAdmin):
    list_display=('title','id','typename')
admin.site.register(Badge,BadgeAdmin)

class Badge_InputAdmin(admin.ModelAdmin):
    list_display=('user','badge')
admin.site.register(Badge_Input,Badge_InputAdmin)

admin.site.register(BadgeType)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Faq)

class CustomUserAdmin(admin.ModelAdmin):
    list_display=('username','department','status','reputation','moderator')
    list_editable=('moderator',)
admin.site.register(CustomUser,CustomUserAdmin)
