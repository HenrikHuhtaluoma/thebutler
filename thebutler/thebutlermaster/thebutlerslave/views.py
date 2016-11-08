#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import json, requests, random, re
import thebutler
from pprint import pprint
from django.views import generic
from django.core.mail import send_mail
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
					
        'taide': 	["""Järjestämme tiloissamme taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
                    """Taiteeseen liittyvissä asiossa ota yhteyttä esimerkki@esimerkki.fi"""],
		'taidetta': ["""Järjestämme tiloissamme taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
                    """Taiteeseen liittyvissä asiossa ota yhteyttä esimerkki@esimerkki.fi"""],
		'taideteos':["""Järjestämme tiloissamme taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
                    """Taiteeseen liittyvissä asiossa ota yhteyttä esimerkki@esimerkki.fi"""],
		'taideteoksia': ["""Järjestämme tiloissamme taidenäyttelyitä ja erilaisia gallerioita, joissa paikalliset lahjakkuudet voivat esitellä töitään.""",
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
					
		'toiminta': ["""Olemme mukana vaikuttamassa erilaisilla festivaaleilla ja näyttelyissä.""",
					"""Toimintamme on Kallion trendikkäintä!"""],
					
		'kuka': ["""Hei! Olen chatbot The Butler, apunasi kun haluat tietää enemmän ravintolastamme tai tehdä tilauksen! Kysy minulta esimerkiksi ruuasta, yrityksestämme tai ravintolasta."""],
		
		'chatbot': ["""Olen siis botti ja osaan vastata sinulle yksinkertaisiin kysymyksiin koskien ravintolaamme. Osaan myös vastaanottaa tilauksen tai varauksen, ja toimittaa sen eteenpäin ravintolan henkilökunnalle."""],

		'teet': ["""Autan sinua kun haluat lisätietoa ravintolastamme ja sen tarjonnasta, tai tehdä tilauksen."""],
		
		'osaat': ["""Autan sinua kun haluat lisätietoa ravintolastamme ja sen tarjonnasta, tai tehdä tilauksen. Voit kysyä minulta ruuasta, yrityksestämme tai ravintolasta."""],
		
   
'hei': ["""Tervehdys! Olen ravintoloita avustava keskustelurobotti Butler. Jos olet tullut betatestaamaan minua, voit halutessasi pyytää minulta ohjeet :)"""],         

'moi': ["""Tervehdys! Olen ravintoloita avustava keskustelurobotti Butler. Jos olet tullut betatestaamaan minua, voit halutessasi pyytää minulta ohjeet :)"""],

'päivää': ["""Tervehdys! Olen ravintoloita avustava keskustelurobotti Butler. Jos olet tullut betatestaamaan minua, voit halutessasi pyytää minulta ohjeet :)"""],

'iltaa': ["""Tervehdys! Olen ravintoloita avustava keskustelurobotti Butler. Jos olet tullut betatestaamaan minua, voit halutessasi pyytää minulta ohjeet :)"""],

'moikka': ["""Tervehdys! Olen ravintoloita avustava keskustelurobotti Butler. Jos olet tullut betatestaamaan minua, voit halutessasi pyytää minulta ohjeet :)"""],

'ohje': ["""Hienoa että haluat testata toiminnallisuuttani! Esitä kuvitteellisen ravintolan asiakasta, ja kysy kysymyksiä joita ravintolan asiakas voisi minulta kysyä.(avainsanat: ruoka, yritys, toiminta, chatbot, osaat)"""],

'ohjeet': ["""Hienoa että haluat testata toiminnallisuuttani! Esitä kuvitteellisen ravintolan asiakasta, ja kysy kysymyksiä joita ravintolan asiakas voisi minulta kysyä.(avainsanat: ruoka, yritys, toiminta, chatbot, osaat)  """],


         }


'''
#incoming message: {
    u'entry': [
        etsessionid(sesid)u'messaging': [
            {u'timestamp': 1475567102490,
             u'message': 
                {u'text': u'Kinkku', u'mid': u'mid.1475567102475:9abfc6de19135f4b79', u'seq': 784},
             u'recipient': {u'id': u'540797152797202'}, 
             u'sender': {u'id': u'1269803593060780'}
            }
        ],
        u'id': u'540797152797202', u'time': 1475567105568
        }
    ], u'object': u'page'
}

incoming message: {u'entry': [{u'messaging': [{u'timestamp': 1475567102490, u'message': {u'text': u'Kinkku', u'mid': u'mid.1475567102475:9abfc6de19135f4b79', u'seq': 784}, u'recipient': {u'id
': u'540797152797202'}, u'sender': {u'id': u'1269803593060780'}}], u'id': u'540797152797202', u'time': 1475567105568}], u'object': u'page'}

'''
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
        #return HttpResponse()
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        print 'incoming message:', incoming_message
        print '1'
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            print '2'
            fb_command_run = 0
            for message in entry['messaging']:
                print '3'
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    print '4'
                    # Print the message to the terminal
                    pprint(message)
                    vastaus = ''
                    if 'id' in entry:
                      print '5'
                      print 'setsession ID', entry['id']
                      thebutler.tb_setsessionid(entry['id'])
                    if 'text' in message['message']:
                      print '6'
                      print 'vastaus tässä', message['message']['text']
                      vastaus = message['message']['text']
                      print 'vertaillaan ID 1', message['recipient']['id']
                      print 'vertaillaan ID 2', entry['id']
                      if message['recipient']['id'] == entry['id']:
                          print 'vertaillaan ID 1', message['recipient']['id']
                          print 'vertaillaan ID 2', entry['id']
                          if 'tilaa' in vastaus.lower():
                              user_details_url = "https://graph.facebook.com/v2.6/" + message['sender']['id']
                              user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAHNADSZAI2gBAJ1DNMBfQsDIAbKZCTixRuZBekezzXyggOWcZCrfUYJrZBhSrkow9ZAxaEPWJMutxZA6Fn0uBfEwetfx3iUasfkM6cT7gxHWtF072ZCXOHZCk7ZAZBi5zAY8y1M0qI5mi9EWPcjtaEtCjyzrsn2vikIbJYw8qEFunWHQZDZD'}
                              user_details = requests.get(user_details_url, user_details_params).json()
                              orderlines = thebutler.tb_answer2()
                              print 'käyttäjän nimi', user_details['first_name']
                              fullname = user_details['first_name'] + " " + user_details['last_name']
                              messagebody = "Asiakas " + fullname + " tilasi tuotteet: \n\n" + "" + str(orderlines)
                              send_mail('Tilaus', messagebody, 'tilaus@huhtaluoma.com', ['henrik.huhtaluoma@gmail.com'])
                          thebutler.tb_command(vastaus)
                          fb_command_run = 1
                          print 'tbCommand ajettu'
                      else:  
                          vastaus = ''
                          print 'tbCommandia ei ajeta'
                      print 'vastaus:[' + vastaus + ']'
                    if 'id' in entry: # uusi rivi                             
                        print 'muuttumaton id', entry['id'] # uusi rivi       
                   #print 'muuttumaton id', entry['messaging']['id']            
                   #print "kayttajan id:", message['sender']['id']
		               #print 'vastaus:', vastaus
                   #print 'muuttumaton id', entry['messaging']['id']
                    print "kayttajan id:", message['sender']['id']
                    #tähän mahdollisesti joku iffi testaamaan että on tb_command ajettu
                    #post_facebook_message(message['sender']['id'], message['message']['text'], entry['id'])
                   #def post_facebook_message(fbid,received_message, sesid):
                    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',message['message']['text']).lower().split()
                    vocabulary_text = ''
                    answerok=0;
                    for token in tokens:
                        if token in vocabulary:
                            vocabulary_text = random.choice(vocabulary[token])
                            answerok=1
                            break
                    if not vocabulary_text:
                        vocabulary_text = "Anteeksi herra, en ymmärtänyt kysymystänne. Osaamisalani ovat: 'ruoka','taide','yritys' ja 'toiminta'"           
                    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAHNADSZAI2gBAJ1DNMBfQsDIAbKZCTixRuZBekezzXyggOWcZCrfUYJrZBhSrkow9ZAxaEPWJMutxZA6Fn0uBfEwetfx3iUasfkM6cT7gxHWtF072ZCXOHZCk7ZAZBi5zAY8y1M0qI5mi9EWPcjtaEtCjyzrsn2vikIbJYw8qEFunWHQZDZD' 
                   
                   # response_msg = json.dumps({"recipient":{"id":message['sender']['id']}, "message":{"text":vocabulary_text}})
                    # JariK 26.9.2016
                    
                    # end of JariK
                    print "answerok", answerok
                    if(answerok==1):
                        print "vocabulary text", vocabulary_text
                        response_msg = json.dumps({"recipient":{"id":message['sender']['id']}, "message":{"text":vocabulary_text}})
                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
                        pprint(status.json())           
                    else:
                      if fb_command_run == 1:
                        thebutler.tb_setsessionid(entry['id'])
                        answer = thebutler.tb_answer()
                        print "answer", answer
                   
                        print "answer lines"
                        answer2 = ''
                        for s in answer:
                            answer2=''.join(str(s))
                            print "answer line (",len(answer2),")", answer2
                            for s2 in answer2.split('\\n',10):
                                print "s2 line:", s2
                                
                            
                                response_msg = json.dumps({"recipient":{"id":message['sender']['id']}, "message":{"text":s2}})
                                status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
                                pprint(status.json())
                              
  
        return HttpResponse()
