from django.views import generic
from django.http.response import HttpResponse
# Create your views here.
class thebutlerview(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '8282657201':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
