#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import json, requests, random, re
import thebutler
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse

reload(sys)  
sys.setdefaultencoding('utf8')

#'ruuat','ruoat'
#'ruuoka','ruoat'
#'safka','ruoat'

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

vocabulary = {        
 'ruoka': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruoat': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruuat': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruoan': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruuan': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruokien': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruokaa': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruokia': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruoassa': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruuassa': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
		'ruuissa': 	["""Tässä kerron kuvailevasti yrityksen ruokatarjonnasta, ja siitä kuinka herkullista se on.""",
                    """Testiravintolamme tarjoaa herkullista brunssia, lounasta ja illallista. Kokeile kuuluisaa kolmen annoksen menuamme!""",
					"""Ruokamme on aina lähituotettua ja kotimaista!""",
					"""Käytämme vain tarkkojen laatuvaatimustemme täyttämiä ruoka-aineita.""",
					"""Tarjoamme myös vegaanisia ja kasvisvaihtoehtoja."""
					],
					
        'taide': 	["""Järjestämme tiloissamma taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
                    """Taiteeseen liittyvissä asiossa ota yhteyttä esimerkki@esimerkki.fi"""],
		'taidetta': ["""Järjestämme tiloissamma taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
                    """Taiteeseen liittyvissä asiossa ota yhteyttä esimerkki@esimerkki.fi"""],
		'taideteos':["""Järjestämme tiloissamma taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
                    """Taiteeseen liittyvissä asiossa ota yhteyttä esimerkki@esimerkki.fi"""],
		'taideteoksia': ["""Järjestämme tiloissamma taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
                    """Taiteeseen liittyvissä asiossa ota yhteyttä esimerkki@esimerkki.fi"""],
		
		
        'yritys': 	["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa."""
					],
					
		'yrityksenne': ["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa."""
					],
		'yrityksen': ["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa."""
					],
		'yrityksessä': ["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa."""
					],
		'yrityksestä': ["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa."""
					],
		'yrityksellä':["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa."""
					],
		'ravintola':	["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa.""",
					"""Ravintolamme tarjoaa herkullista ruokaa niin mukaan kuin paikanpäällä!"""],
		'ravintolanne':	["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa.""",
					"""Ravintolamme tarjoaa herkullista ruokaa niin mukaan kuin paikanpäällä!"""],
		'ravintolan':	["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa.""",
					"""Ravintolamme tarjoaa herkullista ruokaa niin mukaan kuin paikanpäällä!"""],
		'ravintolasta':	["""Yrityksemme on perustettu vuonna 2012.""",
                    """Työllistämme kuusi työntekijää ja ruokaamme on kehuttu muunmuassa Helsingin Sanomissa.""",
					"""Ravintolamme tarjoaa herkullista ruokaa niin mukaan kuin paikanpäällä!"""],
		
		
		'toiminta': ["""Olemme mukana vaikuttamassa erilaisilla festivaaleilla ja näyttelyissä.""",
					"""Toimintamme on Kallion trendikkäintä!"""],
		'toimintamme': ["""Olemme mukana vaikuttamassa erilaisilla festivaaleilla ja näyttelyissä.""",
					"""Toimintamme on Kallion trendikkäintä!"""],
		'toiminnassa': ["""Olemme mukana vaikuttamassa erilaisilla festivaaleilla ja näyttelyissä.""",
					"""Toimintamme on Kallion trendikkäintä!"""],

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
 # JariK 26.9.2016
 thebutler.tb_setsessionid(fbid)
 answer = thebutler.tb_answer()
 print "answer", answer 
 print "kayttajan id:", fbid
 # end of JariK
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
	print 'incoming message:', incoming_message
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
		    vastaus = ''
		    if 'text' in message['message']:
		        vastaus = message['message']['text']
			thebutler.tb_command(vastaus)
		    print 'vastaus:', vastaus
		    print 'muuttumaton id', entry['messaging']['id']
 		    print "kayttajan id:", message['sender']['id']
 		    post_facebook_message(message['sender']['id'], message['message']['text'])

	return HttpResponse()     
