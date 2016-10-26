#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.mail import send_mail

send_mail('subject', 'body of the message', 'tilaus@huhtaluoma.com', ['henrik.huhtaluoma@gmail.com'])