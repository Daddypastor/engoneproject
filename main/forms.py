from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'autofocus':'',
            'required':'',
            'class':"form-control form--control",
            'type':"text", 
            'name':"username",
            'id':"id_username",
            'placeholder':"Enter name",
            })
        self.fields["email"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control",
            'type':"email", 
            'name':"email",
            'id':"id_email",
            'placeholder':"Email address",
            })
        self.fields["password1"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control password-field",
            'type':"password", 
            'name':"password1",
            'id':"id_password1",
            'placeholder':"Password",
            })
        self.fields["password2"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control password-field",
            'type':"password", 
            'name':"password2",
            'id':"id_password2",
            'placeholder':"Password again",
            })
        self.fields["country"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control",
            'type':"text", 
            'name':"country",
            'id':"id_country",
            'placeholder':"Enter Country",
            })
        self.fields["status"].widget.attrs.update({
            'required':'',
            'class':"custom-select custom--select",
            'name':"status",
            'id':"id_status"
            })
        self.fields["department"].widget.attrs.update({
            'required':'',
            'class':"custom-select custom--select",
            'name':"department",
            'id':"id_department"
            })
        self.fields["email_alert"].widget.attrs.update({
            'class':"custom-control-input",
            'type':"checkbox",
            'name':"email_alert",
            'id':"id_email_alert"
            })


    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2','email_alert','status','country','department']

class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs.update({
            'multiple':"",
            'class':"file-upload-input",
            'type':"file", 
            'name':"image",
            })
    class Meta:
        model=Answer
        fields=('detail','image')

class QuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({
            'class':"form-control form--control",
            'type':"text", 
            'name':"title",
            'placeholder':"e.g. Is there an R function for finding the index of an element in a vector?",
            'id':"id_title"
            })
        self.fields["tags"].widget.attrs.update({
            'class':"input-tags input--tags",
            'type':"text", 
            'name':"tags",
            'placeholder':"e.g. javascript",
            'id':"id_tags"
            })
        self.fields["category"].widget.attrs.update({
            'class':"select-container select--container",
            'type':"select", 
            'name':"category",
            'id':"id_category"
            })
        self.fields["image"].widget.attrs.update({
            'multiple':"",
            'class':"file-upload-input",
            'type':"file", 
            'name':"image",
            'id':"id_image"
            })
        self.fields["answer_alarm"].widget.attrs.update({
            'required':'',
            'class':"custom-control-input",
            'type':"checkbox",
            'name':"answer_alarm",
            'id':"id_answer_alarm"
            })
        self.fields["agree_PP"].widget.attrs.update({
            'required':'',
            'class':"custom-control-input",
            'type':"checkbox",
            'name':"agree_PP",
            'id':"id_agree_PP"
            })
    class Meta:
        model=Question
        fields=('title','detail','tags','category','image','answer_alarm','agree_PP')

class QuestEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({
            'class':"form-control form--control",
            'type':"text", 
            'name':"title",
            'placeholder':"e.g. Is there an R function for finding the index of an element in a vector?",
            'id':"id_title"
            })
        self.fields["tags"].widget.attrs.update({
            'class':"form-control form--control",
            'type':"text", 
            'name':"tags",
            'placeholder':"e.g. javascript",
            'id':"id_tags"
            })
        self.fields["category"].widget.attrs.update({
            'class':"select-container select--container",
            'type':"select", 
            'name':"category",
            'id':"id_category"
            })
        self.fields["detail"].widget.attrs.update({
            'class':"form-control form--control user-text-editor",
            'type':"text", 
            'name':"detail",
            'id':"id_detail"
            })
        self.fields["image"].widget.attrs.update({
            'multiple':"",
            'class':"file-upload-input",
            'type':"file", 
            'name':"image",
            'id':"id_image"
            })
        self.fields["answer_alarm"].widget.attrs.update({
            'required':'',
            'class':"custom-control-input",
            'type':"checkbox",
            'name':"answer_alarm",
            'id':"id_answer_alarm"
            })
        self.fields["agree_PP"].widget.attrs.update({
            'required':'',
            'class':"custom-control-input",
            'type':"checkbox",
            'name':"agree_PP",
            'id':"id_agree_PP"
            })
    class Meta:
        model=Question
        fields=('title','detail','tags','category','image','answer_alarm','agree_PP')

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control",
            'type':"text", 
            'name':"username",
            'id':"id_username",
            'placeholder':"Email address",
            })
        self.fields["web_link"].widget.attrs.update({
            'class':"form--control pl-40px",
            'type':"text", 
            'name':"web_link",
            'id':"id_web_link"
            })
        self.fields["twi_link"].widget.attrs.update({
            'class':"form--control pl-40px",
            'type':"text", 
            'name':"twi_link",
            'id':"id_twi_link"
            })
        self.fields["fb_link"].widget.attrs.update({
            'class':"form--control pl-40px",
            'type':"text", 
            'name':"fb_link",
            'id':"id_fb_link"
            })
        self.fields["Ins_link"].widget.attrs.update({
            'class':"form--control pl-40px",
            'type':"text", 
            'name':"Ins_link",
            'id':"id_Ins_link"
            })
        self.fields["ytube_link"].widget.attrs.update({
            'class':"form-control form--control pl-40px",
            'type':"text", 
            'name':"ytube_link",
            'id':"id_ytube_link"
            })
    class Meta:
        model=CustomUser
        fields=(
            'username','bio','profile_pic','web_link',
            'twi_link','ytube_link','Ins_link','fb_link'
            )

class ChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control password-field",
            'type':"password", 
            'name':"old_password",
            'id':"id_old_password",
            'placeholder':"Current password",
            })
        self.fields["new_password1"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control password-field",
            'type':"password", 
            'name':"new_password1",
            'id':"id_new_password1",
            'placeholder':"New password",
            })
        self.fields["new_password2"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control password-field",
            'type':"password", 
            'name':"new_password2",
            'id':"id_new_password2",
            'placeholder':"New password again",
            })
        class Meta:
            model=CustomUser
            fields=('password')

class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control fs-14",
            'type':"text", 
            'name':"name",
            'id':"id_name",
            'placeholder':"e.g. Alex smith",
            })
        self.fields["email"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control fs-14",
            'type':"email",
            'name':"email",
            'id':"id_email",
            'placeholder':" e.g. alexsmith@gmail.com",
            })  
        self.fields["phone"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control fs-14",
            'type':"tel", 
            'name':"phone",
            'id':"id_phone",
            'placeholder':"Your phone number",
            })
        self.fields["message"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control fs-14",
            'type':"text", 
            'name':"message",
            'id':"id_message",
            'placeholder':"Tell us how we can help you...",
            'rows':"6",
            })
    class Meta:
        model=Contact
        fields=('name','email','phone','message')  

class MailMessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control fs-14",
            'type':"text", 
            'name':"title",
            'id':"id_title"
            })
        self.fields["message"].widget.attrs.update({
            'required':'',
            'class':"form-control form--control fs-14",
            'type':"text", 
            'name':"message",
            'id':"id_message",
            'rows':"20",
            })
    class Meta:
        model=MailMessage
        fields=('title','message')
