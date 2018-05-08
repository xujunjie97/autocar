# -*- coding: utf8 -*-
from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator

from first.models import User, order, busniess, car, order_goods
import re
from . import models


# class RegisterForm(forms.Form):
#     userName = fields.CharField(required=True,
#                                 max_length=20,
#                                 strip=True,
#                                 error_messages={
#                                     'required': '用户名不能为空',
#                                     'max_length': '用户名不超过20个字段'
#                                 }, )
#     password = fields.CharField(required=True,
#                                 strip=True,
#                                 max_length=20,
#                                 min_length=6,
#                                 # validators=[
#                                 #     RegexValidator(r'((?=.*\d))^.{6,12}$', '必须包含数字'),
#                                 #     RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$', '必须包含字母'),
#                                 #     RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,12}$', '必须包含特殊字符'),
#                                 #     RegexValidator(r'^.(\S){6,10}$', '密码不能包含空白字符'),
#                                 # ],  # 用于对密码的正则验证
#                                 error_messages={
#                                     'required': '密码不能为空',
#                                     'min_length': '密码长度不少于6个字符',
#                                     'max_length': '密码长度不超过20个字符'
#                                 },
#                                 )
#     repassword = fields.CharField(
#         required=True,
#         strip=True,
#         max_length=20,
#         min_length=6,
#         error_messages={'required': '请再次输入密码！'},
#     )
#     userImage = fields.ImageField()
#     name = fields.CharField(max_length=30)
#     addrId = fields.IntegerField()
#
#     def clean_userName(self):
#         userName = self.cleaned_data.get('userName')
#         users = models.User.objects.filter(userName=userName).count()
#         if users:
#             raise ValidationError('用户已存在')
#         return userName
#
#     def clean_repassword(self):
#         password = self.cleaned_data.get('password')
#         repassword = self.cleaned_data.get('repassword')
#         if password and repassword:
#             if password != repassword:
#                 raise ValidationError('两次密码不匹配.')
#
#     # def clean(self):
#     #     self.clean_repassword()
#
#
# class loginForm(forms.Form):
#     userName = fields.CharField(required=True,
#                                 max_length=20,
#                                 strip=True,
#                                 error_messages={
#                                     'required': '用户名不能为空',
#                                 }, )
#     password = fields.CharField(required=True,
#                                 strip=True,
#                                 max_length=20,
#                                 min_length=6,
#                                 error_messages={
#                                     'required': '密码不能为空',
#                                 },
#                                 )
#
#     def clean(self):
#         userName = self.cleaned_data.get('userName')
#         password = self.cleaned_data.get('password')
#         user = models.User.objects.filter(userName=userName)
#         if userName and password:
#             if not user:
#                 raise ValidationError('用户名不存在')
#             elif password != user.password:
#                 raise ValidationError('密码错误!')

class RegisterForm(forms.ModelForm):
    password2 = fields.CharField(max_length=20, min_length=6)

    class Meta:
        model = User
        fields = ('userName', 'password', 'password2')

    def clean_userName(self):
        cleaned_data = self.cleaned_data['userName']
        # 格式转化
        num = cleaned_data.encode("utf-8")
        regex = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        if cleaned_data.isdigit():
            phonematch = regex.match(num)
            print(phonematch)
            if phonematch:
                return int(cleaned_data)
            else:
                raise ValidationError("电话号码格式不正确.")
        else:
            raise ValidationError("必须是数字！")


class LoginForm(forms.Form):
    userName = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class modifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class uploadImgForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatarUrl',)


class userInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('nickName', 'addressId')


class orderForm(forms.ModelForm):
    # userName = fields.CharField(max_length=20)
    # carId = fields.IntegerField()
    # payMoney = fields.DecimalField(max_digits=5, decimal_places=2)
    # useraddr = fields.IntegerField()

    class Meta:
        model = order
        fields = ('userName', 'busniessId', 'payMoney', 'useraddr', 'carId')

    def __init__(self, *args, **kwargs):
        super(orderForm, self).__init__(*args, **kwargs)
    #     self.fields['userName'].queryset = User.objects.values_list('userName', flat=True)
    #     self.fields['busniessId'].queryset = busniess.objects.values_list('busniessId')
    #     self.fields['carId'].queryset = car.objects.values_list('carId')

    # def clean_userName(self):
    #     userName = self.cleaned_data['userName']
    #     user = User.objects.get(userName=userName)
    #     if user:
    #         return int(user.userName)
    #     else:
    #         raise ValidationError('用户名不存在')

    # def clean_busniessId(self):
    #     busniessNum = self.cleaned_data['busniessId']
    #     busniess2 = busniess.objects.get(pk=busniessNum)
    #     if busniess2:
    #         return int(busniessNum)
    #     else:
    #         raise ValidationError('商家不存在')

    # def clean_carId(self):
    #     carId = self.cleaned_data['carId']
    #     car2 = car.objects.get(pk=int(carId))
    #     if car2:
    #         return int(carId)
    #     else:
    #         raise ValidationError('小车不存在')


class orderGoodsForm(forms.ModelForm):
    class Meta:
        model = order_goods
        fields = ('orderId', 'goodsId', )