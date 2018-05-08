# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import Client
from django.test import TestCase

from django.test import TestCase
from django.conf import settings
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'autocar.settings'


# Create your tests here.

# class firstTest(TestCase):
#     c = Client()
#     csrf_client = Client(enforce_csrf_checks=True)
#     response = c.post('http://127.0.0.1:8000/first/userlogin', {'username': '17680643321', 'password': '123412'})
#     print(response)
#     print(response.status_code)
#     print(response)


class second(TestCase):
    c = Client()
    csrf_client = Client(enforce_csrf_checks=True)
    with open('first/static/123.jpg') as fp:
        c.post('http://127.0.0.1:8000/first/updataImage', {'username': '17680643321', 'userImage': fp})


