# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import time
import json

# import datetime
from datetime import datetime
from django.contrib import auth
from django.db import transaction
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View

from Forms import RegisterForm, LoginForm, modifyPwdForm, uploadImgForm, userInfoForm, orderForm, orderGoodsForm
from models import User, order, order_goods, goods
import redis


# Create your views here.


def index(req):
    return render(req, 'first/register.html')


def success(req):
    return render(req, 'first/success.html')


def login(req):
    return render(req, 'first/login.html')


# 注册
def register_view(req):
    # users = User.objects.all()
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = User()
            cleaned_data = form.cleaned_data
            user.userName = cleaned_data['userName']
            if User.objects.filter(userName=user.userName):
                return render(req, 'first/register.html', {'form.user.errors': "用户已存在"})
            user.password = cleaned_data['password']
            password2 = cleaned_data['password2']
            if user.password != password2:
                return render(req, 'first/register.html', {'msg': "两次密码输入不相同"})
            user.save()
            return render(req, 'first/success.html')
        else:
            context = {
                'form': form,
            }
        return render(req, 'first/register.html', context)


def userlogin_view(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            userName = form.cleaned_data['userName']
            password = form.cleaned_data['password']
            if User.objects.filter(userName=userName, password=password):
                # auth.login(req, user)
                conn = redis.Redis(host='127.0.0.1', port=6379)
                conn.hset('login', 'userName', userName)

                return render(req, 'first/success.html')
            else:
                return render(req, 'first/login.html', {'msg': '账号或密码错误'})

        else:
            context = {
                'form': form,
            }
        return render(req, 'first/login.html', context)


def userlogim_out(req):
    # auth.logout(req)
    userName = req.POST.get("userName", "")
    conn = redis.Redis(host='127.0.0.1', port=6379)
    conn.hdel('login', userName)

    return HttpResponseRedirect(reverse('login'))


def modifyPwd(req):
    return render(req, 'first/password_reset.html')


def modifyPwd_view(req):
    if req.method == 'POST':
        form = modifyPwdForm(req.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            userName = req.POST.get("userName", "")
            if password1 != password2:
                return render(req, 'first/password_reset.html', {"msg": "两次密码输入不相同"})
            user = User.objects.get(userName=userName)
            user.password = password2
            user.save()
            return render(req, 'first/login.html')
        else:
            return render(req, 'first/password_reset.html', {"msg": "出现异常"})


def uploadImg(req):
    userName = req.POST.get("userName", "")
    return render(req, 'first/updataImage.html', {"userName": userName})


def uploadImg_view(req):
    if req.method == 'POST':
        print(req.FILES['avatarUrl'])
        new_img = uploadImgForm(req.POST, req.FILES)
        if new_img.is_valid():
            userName = req.POST.get("userName", "")
            user = User.objects.get(userName=userName)
            user.avatarUrl = new_img.cleaned_data['avatarUrl']
            user.save()
        return render(req, 'first/success.html', {'image': user.avatarUrl})


def userInfo(req):
    return render(req, 'first/userinfo.html')


def userInfo_view(req):
    if req.method == 'POST':
        form = userInfoForm(req.POST)
        if form.is_valid():
            user = User()
            user.nickName = form.cleaned_data['nickName']
            user.addressId = form.cleaned_data['addressId']
            user.save()
            return render(req, 'first/success.html')
        return render(req, '/', {'msg': '输入信息错误'})


#
# class MyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         else:
#             return json.JSONEncoder(self, obj)


class order_view(View):

    @staticmethod
    def get(req):
        return render(req, 'first/order.html')

    @staticmethod
    def post(req):
        form = orderForm(req.POST)
        if form.is_valid():
            orders = order()
            orders.userName_id = form.cleaned_data['userName']
            orders.busniessId = form.cleaned_data['busniessId']
            orders.carId = form.cleaned_data['carId']
            orders.payMoney = form.cleaned_data['payMoney']
            orders.useraddr = form.cleaned_data['useraddr']
            # orders.ordersTime = datetime.strftime("%H:%M:%S", datetime.now())
            orders.ordersTime = datetime.now().strftime("%H:%M:%S")
            orders.orderId = random.randint(10000, 99999)
            time1 = datetime.now()
            orders.save()
            list = req.POST.getlist('foods')
            msg = []
            goodlist = []
            for food in list:
                print(food)
                goods1 = goods.objects.get(goodsId=food)
                goods1.quantity = goods1.quantity - 1
                if goods1.quantity < 0:
                    transaction.rollback()
                    orders.delete()
                    msg.append('商品' + goods1.name + '已售完')
                    return render(req, 'first/order.html', {'msg': msg})
                goods1.sales_volume = goods1.sales_volume + 1
                try:
                    goods1.save()
                except:
                    transaction.rollback()
                    orders.delete()
                    msg.append('商品选择失败')
                    return render(req, 'first/order.html', {'msg': msg})
                else:
                    transaction.commit()
                orderGoods = order_goods(orderId_id=orders.orderId, goodsId_id=food)
                try:
                    orderGoods.save()
                except:
                    transaction.rollback()
                    orders.delete()
                    msg.append('下单失败')
                    return render(req, 'first/order.html', {'msg': msg})
                else:
                    transaction.commit()

                goodlist.append(goods1.name)
            time1 = time1.strftime('%Y-%m-%d %H:%M:%S')
            push = [{'orderId': orders.orderId,
                     'carId': req.POST.get("carId", ""),
                     'userName': req.POST.get("userName", ""),
                     'payMoney': req.POST.get("payMoney", ""),
                     'orderTime': time1,
                     'useraddr': req.POST.get("useraddr", ""),
                     'goods': goodlist}]
            conn = redis.Redis(host='127.0.0.1', port=6379)
            json_str = json.dumps(push)

            conn.publish('order', json_str)

            return render(req, 'first/success.html')
        else:
            return render(req, 'first/order.html', {'form': form})
