# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.db import models


# Create your models here.
# python manage.py makemigrations +app
# python manage.py migrate

class address(models.Model):
    addrId = models.IntegerField(verbose_name="地址ID", primary_key=True)
    areaId = models.IntegerField(verbose_name="园区ID")
    detailAddress = models.CharField(max_length=30, verbose_name="建筑物")
    phoneNumber = models.CharField(max_length=30, verbose_name="手机号码")

    def __str__(self):
        return self.addrId


class User(models.Model):
    # userId = models.AutoField(verbose_name="主键", primary_key=True)
    userName = models.CharField(max_length=20, verbose_name="用户名(电话)", primary_key=True)
    password = models.CharField(max_length=20, verbose_name="密码")
    avatarUrl = models.ImageField(upload_to='first/Userimage/', max_length=50, verbose_name="用户头像", null=True)
    nickName = models.CharField(max_length=30, verbose_name="用户昵称", null=True)
    addressId = models.ForeignKey(address, verbose_name="地址id", null=True)

    def __str__(self):
        return self.userName


class busniess(models.Model):
    busniessId = models.AutoField(verbose_name="主键", primary_key=True)
    name = models.CharField(max_length=20, verbose_name="商家名", unique=True)
    busniessName = models.CharField(max_length=20, verbose_name="商家登录名", unique=True)
    password = models.CharField(max_length=20, verbose_name="密码")
    avatarUrl = models.ImageField(upload_to='first/busniessImage', max_length=50, verbose_name="商家头像", null=True)
    addressId = models.ForeignKey(address)
    isopen = models.IntegerField(choices=(
        (0, '营业中'),
        (1, '停业中')
    ), default=0)

    def __str__(self):
        return self.busniessName


class goods(models.Model):
    goodsId = models.AutoField(verbose_name="主键", primary_key=True)
    name = models.CharField(max_length=30, verbose_name="商品名称", unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="商品价格")
    quantity = models.IntegerField(verbose_name="商品数量")
    picUrl = models.ImageField(upload_to='first/goodsImag', max_length=50, verbose_name="商品图片", null=True)
    sales_volume = models.IntegerField(verbose_name="销售量")

    def __str__(self):
        return self.goodsId


class area(models.Model):
    areaId = models.IntegerField(verbose_name="园区ID", primary_key=True)
    areaName = models.CharField(max_length=20, verbose_name="园区名")

    def __str__(self):
        return self.areaId


class car(models.Model):
    carId = models.IntegerField(verbose_name="小车ID", primary_key=True)
    areaId = models.ForeignKey(area, verbose_name="园区ID")
    capability = models.IntegerField(verbose_name="小车总容量")
    usedCapability = models.IntegerField(verbose_name="已用容量", default=0)
    status = models.IntegerField(choices=(
        (0, '停用'),
        (1, '使用中')
    ), default=0, verbose_name='小车状态')
    currentPosition = models.CharField(max_length=30, verbose_name="小车位置", null=True)

    def __str__(self):
        return self.carId


class order(models.Model):
    orderId = models.CharField(max_length=30, verbose_name="订单ID", primary_key=True)
    userName = models.ForeignKey(User, verbose_name="用户名")
    busniessId = models.ForeignKey(busniess, verbose_name="商家ID")
    carId = models.ForeignKey(car, verbose_name='小车ID')
    payMoney = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="支付金额")
    useraddr = models.ForeignKey(address, verbose_name="用户收货地址")
    ordersTime = models.TimeField(auto_now_add=True, verbose_name="订单创建时间")
    completeTime = models.TimeField(auto_now_add=True, null=True, verbose_name="订单完成时间")
    status = models.IntegerField(choices=(
        (0, '已提交'),
        (1, '已接受'),
        (2, '已完成')
    ), default=0, verbose_name="订单状态")

    def __str__(self):
        return self.orderId


class order_goods(models.Model):
    serialNUmber = models.AutoField(verbose_name="序列号", primary_key=True)
    orderId = models.ForeignKey(order)
    goodsId = models.ForeignKey(goods)

    def __str__(self):
        return self.serialNUmber


