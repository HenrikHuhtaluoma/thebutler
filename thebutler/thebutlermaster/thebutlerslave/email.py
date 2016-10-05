#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.mail import send_mail

send_mail(
    'Uusi tilaus',
    'Here is the message.',
    'tilaus@tilaus.com',
    ['henrik.huhtaluoma@gmail.com'],
    fail_silently=False,
)
