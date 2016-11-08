#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.views.generic import View
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect

EmailMessage('subject', 'body of the message', 'tilaus@huhtaluoma.com', ['henrik.huhtaluoma@gmail.com'])