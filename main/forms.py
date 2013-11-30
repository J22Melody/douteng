#coding=utf8

from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from models import *


class LoginForm(forms.Form):
    username=forms.CharField(label=u"用户名",max_length=12,error_messages={'required': '用户名不能为空'})
    password=forms.CharField(label=u"密码",max_length=16,widget=forms.PasswordInput(),error_messages={'required': '密码不能为空'})  

    def clean_username(self):  
        username = self.cleaned_data['username']  
        users = User.objects.filter(username=username)  
        if not users:              
            raise forms.ValidationError("用户名不存在")
        return username  

    def clean_password(self):
        password = self.cleaned_data['password']
        user = authenticate(username=self.cleaned_data.get('username'), password=password)
        if user is None: 
            raise forms.ValidationError("用户名密码不匹配")
        return password

class RegisterForm(forms.Form):
    username = forms.CharField(label=u"用户名",max_length=12,error_messages={'required': '用户名不能为空'})
    password = forms.CharField(label=u"密码",max_length=16,widget=forms.PasswordInput(),error_messages={'required': '密码不能为空'})  
    password2 = forms.CharField(label=u"重复密码",max_length=16,widget=forms.PasswordInput(),error_messages={'required': '请再次输入密码'}) 
    introduction = forms.CharField(label=u"个人说明",widget=forms.Textarea,required=False)
    portrait = forms.ImageField(label=u"头像",required=False)
     
    def clean_username(self):  
        username = self.cleaned_data['username']  
        users = User.objects.filter(username=username)  
        if users:              
            raise forms.ValidationError("用户名已被使用")
        return username 

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if password2 != self.cleaned_data.get('password'):
            raise forms.ValidationError("两次输入密码不一致")
        return password2
   
# class ModifyForm(forms.Form):
#     username = forms.CharField(label=u"用户名",max_length=12,error_messages={'required': '用户名不能为空'})
#     password = forms.CharField(label=u"密码",max_length=16,widget=forms.PasswordInput(),error_messages={'required': '密码不能为空'})  
#     password2 = forms.CharField(label=u"重复密码",max_length=16,widget=forms.PasswordInput(),error_messages={'required': '请再次输入密码'}) 
#     sex = forms.ChoiceField(label=u"性别",widget=forms.RadioSelect,choices=Profile.SEX_CHOICES,initial=0)
#     email = forms.EmailField(label=u"电子邮件",max_length=20,error_messages={'required': '电子邮件不能为空','invalid': '请输入合法的电子邮件'})
#     first_name = forms.CharField(label=u"大名",max_length=12,required=False)  
#     last_name = forms.CharField(label=u"小名",max_length=12,required=False)  
#     phone = forms.CharField(label=u"电话号码",max_length=20,required=False)  
#     introduction = forms.CharField(label=u"个人说明",widget=forms.Textarea,required=False)
#     portrait = forms.ImageField(label=u"头像",required=False)

#     def clean_password2(self):
#         password2 = self.cleaned_data['password2']
#         if password2 != self.cleaned_data.get('password'):
#             raise forms.ValidationError("两次输入密码不一致")
#         return password2 
