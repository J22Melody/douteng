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
   
class QuestionForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.max_score = kwargs.pop('max_score')
        super(QuestionForm,self).__init__(*args,**kwargs)

    title = forms.CharField(label=u"标题",max_length=50,error_messages={'required': '标题不能为空'})
    content = forms.CharField(label=u"内容",widget=forms.Textarea,required=False)
    score = forms.IntegerField(label=u"悬赏分值",initial=10,min_value=0,error_messages={'required': '请输入分值','min_value':'分值必须是正整数呢','invalid':'分值必须是正整数呢'})
    topic = forms.ModelMultipleChoiceField(label=u"所属话题",queryset=Topic.objects.all(),required=False)

    def clean_score(self):
        score = self.cleaned_data['score']  
        if score > self.max_score:
            raise forms.ValidationError("剩余分数不够啦")
        return score
