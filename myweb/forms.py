from django import forms


# django自带的from表单,在此作为登录表单使用
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名:', required=True)  # required=True/False 是否必填字段
    password = forms.CharField(label='密码:', widget=forms.PasswordInput)
