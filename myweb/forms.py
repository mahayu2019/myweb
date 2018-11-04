from django import forms
from django.contrib import auth


# django自带的from表单,在此作为登录表单使用
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名:', required=True)  # required=True/False 是否必填字段
    password = forms.CharField(label='密码:', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误!')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data
