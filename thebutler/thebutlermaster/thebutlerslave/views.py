#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import json, requests, random, re
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

vocabulary = {
         'ruoka': ["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!"""],
         'taide': ["""Järjestämme tiloissamma taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
                    """Taiteeseen liittyvissä asiossa ota yhteyttä esimerkki@esimerkki.fi"""],
         'yritys': ["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa."""],
	
	 'toiminta': ["""Olemme mukana vaikuttamassa erilaisilla festivaaleilla ja näyttelyissä.""",
		      """Toimintamme on Kallion trendikkäintä!"""]

         }

def post_facebook_message(fbid, recevied_message):
 tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
 vocabulary_text = ''
 for token in tokens:
     if token in vocabulary:
         vocabulary_text = random.choice(vocabulary[token])
         break
 if not vocabulary_text:
     vocabulary_text = "Anteeksi herra, en ymmärtänyt kysymystänne. Osaamisalani ovat: 'ruoka','taide','yritys' ja 'toiminta'"           
 post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAHNADSZAI2gBAIrlsOJEnnC4Nl2aqBtoZA15MgIys06pLgsngJpQ2yg3KFNNhceBnNdZCJpjj92KQxKy8kHJZCoZAJa59gYWcBylimZCcIiNoi67OkI1CZAIHdblWj6UkdhYv8ZAWCWma7gl699D9PY7Bli1VRfoqwEXlH16jwSMgZDZD' 
 response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":vocabulary_text}})
 status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
 pprint(status.json())           
  


# Create your views here.
class thebutlerview(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '12345678910':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

     # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])     
        return HttpResponse()
