#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

valinnat=[]
valitut=[]
global sessionid
global valikko

sessionidsep='/'

def tb_init(): # 23.9.2016 JariK

    global products
    global sessionid
    global valikko

    print "init"
    
    fileid=open("/var/thebutler/thebutler.dat","r")
    products=fileid.readlines()
    fileid.close()
    
    sessionid="123456"
    valikko=0
    
def tb_setsessionid(sessionid2):

    global sessionid
    print "sessionid-thebutler", sessionid2
    sessionid=sessionid2


def isnum(value):

    try:
        int(value)
        return True
    except:
        return False


def tb_clear():

    global sessionid
    global valitut

    print "clearing usermenu"
    for index in range(len(valitut),0):
        print "remove"+valitut[index]+valitut[index].split(',',1)[0]
        if(valitut[index].split(sessionidsep,1)[0]==sessionid):
            print "poistettu"
            valitut.remove(valitut[index])


def tb_clear_valinnat(): # 21.9.2016 JariK 

    global sessionid
    global valinnat

    for s in reversed(valinnat): # New version 6.10.2015 JariK
        if(s.split(sessionidsep,1)[0]==sessionid):
            print "poistettu",s
            valinnat.remove(s)
''' Old 1
    print "clearing usermenu for session 3 ", sessionid
    for index in range(len(valinnat),0):
        print index
        print "remove"+valinnat[index]+valinnat[index].split(',',1)[0]
        print "*", valinnat[index].split(',',1)[0],sessionid
        if(valinnat[index].split(',',1)[0]==sessionid):
            print "poistettu"
            valinnat.remove(valinnat[index])
'''


def tb_clear_valitut(): # 23.9.2016 JariK 

    global sessionid
    global valitut

    for s in reversed(valitut):
        if(s.split(sessionidsep,1)[0]==sessionid):
            print "poistettu",s
            valitut.remove(s)

''' Old 1
    print "clearing usermenu for session", sessionid
    for index in range(len(valitut),0):
        print "remove"+valitut[index]+valitut[index].split(',',1)[0]
        if(valitut[index].split(',',1)[0]==sessionid):
            print "poistettu"
            valitut.remove(valitut[index])
'''


def tb_list_products():

    global products

    print "tuotteet"
    for s in products:
        sys.stdout.write(s)


def tb_list_valinnat():

    global valinnat

    print "valinnat"
    for s in valinnat:
        sys.stdout.write(s)


def tb_list_valitut():

    global valitut

    print "valitut"
    for s in valitut:
        sys.stdout.write(s)


def tb_haku(hakujono):
    global sessionid
    global products
    global valinnat
    global valikko
    global valitut

    c=1;
    sanat=hakujono.split(' ',10)

    print sanat

    ok=0;

    # Check that command contains keywords (kinkku, margaretam etc.

    for index in range(len(sanat)):
        if not isnum(sanat[index]):
            if not sanat[index][0]=='+':
                ok=1;


    if(ok==1):
        print "pizzojen haku menu:hun"
        tb_clear_valinnat()
        valikko=1
	print "valikko", valikko
        # This routine goes thru product lines, and adds those lines that have all
        # keywords given in command line. Comments added. 23.9.2016 JariK

        # Go thru product lines
        for s in products:
            ok=1;
            # Go thru command words
            for index in range(len(sanat)): 
                if not sanat[index] == '': # 16.9.2016 JariK
                    # If word is not numeric
                    if not isnum(sanat[index]): 
                        # if it not topping
                        if not sanat[index][0]=='+':
                            # if it present in
                            if sanat[index].lower() not in s.lower(): 
                                ok=0;
        
            if(ok==1):
                sys.stdout.write(str(c)+". ")
                sys.stdout.write(s)
                c+=1
                string = sessionid+sessionidsep+s
                valinnat.append(string)

    tb_list_valinnat()


def tb_valitut(komentojono):
    global sessionid
    global valinnat
    global valitut
    global valikko
    global products

    sanat=komentojono.split(' ',10)

    ok=0;
    for s in range(len(sanat)): # 16.9.2016 JariK
        if (isnum(sanat[s])):
            ok=1;

    if ok==1:

        print "pizzojen valinta, komentojono", komentojono
        valikko=2
        # This routine goes thru products selected with keywords,
        # and writes products matching index in given by user
        # command line.

        # Go thru all words in command line
        for index in range(len(sanat)):

            # If this word is numeric, find x th product
            # to valitut array.

            print "tb_valitut/valinnat", valinnat
            if(isnum(sanat[index])):
                c=0 # c has number of line in this session
                d=0 # d has index into array
                e=int(sanat[index]) # e has number user gave
                while True and d<len(valinnat):
                    if(valinnat[d].split(sessionidsep,1)[0]==sessionid):
                        c=c+1
                    if(c==e):
                        break;
                    d=d+1

                if(d<len(valinnat)):
                   valitut.append(valinnat[d])
    

#    tb_list_valitut()


def tb_lisataytteet(komentojono):

    global valitut
    global valinnat
    global sessionid
    global products
    global valikko

    sanat=komentojono.split(' ',10)

    ok=0;
    
    # For this part to be run, we need extra toppings
    # in command

    for s in range(len(sanat)): # 16.9.2016 JariK
        if sanat[s][0]=='+':
            ok=1;

    if ok == 1:

        valikko=2
        print "lisataytteet pizzoille"        
        d=-1
        c=-1

        # Go thru command words, and for numeric word, find xth products
        # and for words that have '+' sign in the beginning, find
        # topping, and add topping line after pizza line found earlier
        #
        # for example
        #    1 +garlic 2 +bluecheese = add garlic to product one, and
        #                              cluecheese to product 2

        # Go thru words of the command

        for s in range(len(sanat)):
            if(isnum(sanat[s])):
                c=0; # c has index into list valinnat
                d=0; # d has pizzaid (pizza=pizza+lisataytteet
                e=int(sanat[s]);

#                print "e", e, "len valitut 1", len(valitut)
                
                # Find c:th pizza

                while(c < len(valitut) and d<e): # 20.9.2016 JariK */
                    if(valinnat[d].split(sessionidsep,1)[0]==sessionid):
#                        print valitut[c]

                        # This line is product

                        if 'pizza' in valitut[c]:
#                            print "valittu"
                            d=d+1
                    c=c+1

#                print "c", c, "d", d, "len valitut 2", len(valitut)

                # Skip toppings

                while(c < len(valitut)):
                    if(valinnat[d].split(sessionidsep,1)[0]==sessionid):
#                        print valitut[c]
                        if 'pizza' in valitut[c]: # This line is pizza
                            break;
                    c=c+1

#                print "c:",c,"d:",d

            # If word is topping (+garlic +gorgonzola) */
            
            elif(sanat[s][0]=='+'):
                
                # C should contain line that our topping
                # should be inserted before. (See chapter just before this
                # However assume first pizza if not available.

                if(c==-1):
                    c=0;

                hakusana=sanat[s];
                while(hakusana[0]=='+'):
                    hakusana=hakusana[1:]
                print hakusana
                for t in products:
                    if not 'pizza' in t:
                        if hakusana.lower() in t.lower():
#                            print "*3",hakusana
#                            print "*4",t
                            if(c!=-1):
                                string = sessionid+sessionidsep+t
#                                print "lisätty",string
                                if(c<len(valitut)): # 21.9.2016 JariK
                                    valitut.insert(c,string)
                                else:
                                    valitut.append(string)
                            print t
                        
#    tb_list_valitut()


def tb_command(custline):

    global valitut
    global valikko

    print "sessionid-thebutler command", sessionid
    print(custline)

    custline=custline.replace("(",' ') # 23.9.2016 JariK
    custline=custline.replace(")",' ') # 23.9.2016 JariK
    custline=custline.replace("[",' ') # 23.9.2016 JariK
    custline=custline.replace("]",' ') # 23.9.2016 JariK
    custline=custline.replace("'",' ') # 23.9.2016 JariK
    custline=custline.replace('{',' ') # 23.9.2016 JariK
    custline=custline.replace('}',' ') # 23.9.2016 JariK
    custline=custline.replace("u'",' ') # 23.9.2016 JariK
    custline=custline.replace("'",' ') # 23.9.2016 JariK
        
    custline=custline.replace('+',' +') # 23.9.2016 JariK

    # Replace '+':ses with space plus (to fix commands like 1+garlic)
    
    custline=custline.replace('+',' +') # 23.9.2016 JariK

    #replace ',' with space for command like "kinkku, ananas, aurajuusto"

    custline=custline.replace(',',' ')

    # Replace '+' space with '+' this concatenates '+' with following topping
    # While loop repeats until not found.

    custlineb=custline;
    custline=''
    while(custline!=custlineb):
        custline=custlineb
        custlineb=custline.replace('+ ','+')

    custline=custlineb

    # Replace two spaces with one
 
    custlineb=custline;
    custline=''
    while(custline!=custlineb):
        custline=custlineb
        custlineb=custline.replace('  ',' ')

    custline=custline.replace('  ',' ') # 23.9.2016 JariK

    # Remove spaces in beginning of command
    
    while(len(custline)>0 and custline[0]==' '):
        custline=custline[1:]

    # Remove spaces in end of command

    while(len(custline)>0 and custline[-1]==' '):
        custline=custline[:-1]

    print "tb_command",custline
    if not (custline==''):
      print 'tilaus tässä', custline
    
      if 'tilaa' in custline.lower():
        tilaus=[]
        valikko=10      
        c=1;
        for a2 in valitut:
          if(a2.count(sessionidsep)>0):
            tilaus.append(str(c)+'. '+a2.split(sessionidsep,40)[1])
          else:
            tilaus.append(a2)
          c=c+1
        print "valmis tilaus", tilaus
        print "tilausvalikko", valikko
        tb_clear_valinnat()
        tb_clear_valitut()
      else:  
        tb_haku(custline)
        tb_valitut(custline)
        tb_lisataytteet(custline)
        for index in range(len(valitut)):
            print valitut[index]

def tb_answer(): # 27.9.2016 JariK 

    global valikko
    global valinnat
    global valitut
    global products
    print "sessionid-thebutler answer", sessionid
    print "valikko", valikko
    print "valinnat", valinnat
    print "valitut", valitut
    answer=[]    
    if(valikko==0):

      c=1;
      for a2 in products:
        if(a2.count(sessionidsep)>0):
          answer.append(str(c)+'. '+a2.split(sessionidsep,40)[1])
        else:
          answer.append(a2)
        c=c+1

    elif(valikko==1):

      c=1;
      for a2 in valinnat:
        if(a2.count(sessionidsep)>0):
          answer.append(str(c)+'. '+a2.split(sessionidsep,40)[1])
        else:
          answer.append(a2)
        c=c+1
    
    elif(valikko==2):

      c=1;
      for a2 in valitut:
        if(a2.count(sessionidsep)>0):
          answer.append(str(c)+'. '+a2.split(sessionidsep,40)[1])
        else:
          answer.append(a2)
        c=c+1
        
    elif(valikko==10):
        answer=[]
        answer.append('tilattu')

    print "anssi", answer

    return(answer)

def tb_answer2(): # 27.9.2016 JariK 

    global valitut
    print "sessionid-thebutler answer", sessionid
    print "valitut", valitut
    answer=[]    

    c=1;
    for a2 in valitut:
      if(a2.count(sessionidsep)>0):
        answer.append(str(c)+'. '+a2.split(sessionidsep,40)[1])
      else:
        answer.append(a2)
      c=c+1
        

    print "anssi", answer

    return(answer)
    
print "thebutler"
print 'tuotteiden valinta raaka-aineiden tai nimen mukaan: "kinkku ananas"'
print 'valinta listasta: "2"'
print 'lisätäytteet "1+valkosipuli"'
print 'pizzan valinta ja lisataytteet: "hollywood 1 1+valkosipuli"'

def comp(list1, list2):

  ok=1
  if len(list1) != len(list2):
      ok=0;
      return(ok)
  
  for elem in list1:
      if not elem in list2:
          ok=0

  return ok

def tb_test():

    global products
    global valinnat
    global valitut

    print 'testing....'

    testsfail=0

    tb_setsessionid('1234')
    products= [
        'Tuote 1 a,b,c,d',
        'Tuote 2 a,b,c',
        'Tuote 3 a,b',
        'Tuote 4 a',
    ]
    tb_command('a')
    if comp(tb_answer(), ['1. Tuote 1 a,b,c,d', '2. Tuote 2 a,b,c', '3. Tuote 3 a,b', '4. Tuote 4 a']):
      print 'test1ok'
    else:
      print 'test1fail'
      testsfail=1

    tb_command('b')
    if comp(tb_answer(), ['1. Tuote 1 a,b,c,d', '2. Tuote 2 a,b,c', '3. Tuote 3 a,b']):
      print 'test2ok'
    else:
      print 'test2fail'
      testsfail=1
    
    tb_command('c')
    if comp(tb_answer(), ['1. Tuote 1 a,b,c,d', '2. Tuote 2 a,b,c']):
      print 'test3ok'
    else:
      print 'test3fail'
      testsfail=1

    tb_command('d')
    if comp(tb_answer(), ['1. Tuote 1 a,b,c,d']):
      print 'test4ok'
    else:
      print 'test4fail'
      testsfail=1

    valitut=[]
    tb_command('a,1')
    if comp(tb_answer(), ['1. Tuote 1 a,b,c,d']):
      print 'test5ok'
    else:
      print 'test5fail'
      testsfail=1

    valitut=[]
    tb_command('a,2')
    if comp(tb_answer(), ['1. Tuote 2 a,b,c']):
      print 'test6ok'
    else:
      print 'test6fail'
      testsfail=1

    valitut=[]
    tb_command('a,3')
    if comp(tb_answer(), ['1. Tuote 3 a,b']):
      print 'test7ok'
    else:
      print 'test7fail'
      testsfail=1

    valitut=[]
    tb_command('a,4')
    if comp(tb_answer(), ['1. Tuote 4 a']):
      print 'test8ok'
    else:
      print 'test8fail'
      testsfail=1

    if(testsfail==1):
        print '============Tests FAIL=========='
    else: 
        print '===========Tests OK==========='

    products = []
    valitut = []
    valinnat = []

tb_test()
tb_init()
'''
while(True):
    custline=raw_input('Enter your input:')
    if not (custline==''):
        tb_command(custline)
        answer=tb_answer()
        print answer
    elif(valikko==1):
        tb_list_products()
        valikko=(valikko+1) % 3
    elif(valikko==2):
        tb_list_valinnat()
        valikko=(valikko+1) % 3
    elif(valikko==3):
        tb_list_valitut()
        valikko=(valikko+1) % 3
'''
