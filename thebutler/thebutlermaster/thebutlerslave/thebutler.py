#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

valinnat=[]
valitut=[]
global sessionid
global valikko

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

    print "clearing usermenu"
    for index in range(len(valitut),0):
        print "remove"+valitut[index]+valitut[index].split(',',1)[0]
        if(valitut[index].split(',',1)[0]==sessionid):
            print "poistettu"
            valitut.remove(valitut[index])


def tb_clear_valinnat(): # 21.9.2016 JariK 

    print "clearing usermenu"
    for index in range(len(valinnat),0):
        print "remove"+valinnat[index]+valinnat[index].split(',',1)[0]
        if(valinnat[index].split(',',1)[0]==sessionid):
            print "poistettu"
            valinnat.remove(valinnat[index])


def tb_clear_valitut(): # 23.9.2016 JariK 

    print "clearing usermenu"
    for index in range(len(valitut),0):
        print "remove"+valitut[index]+valitut[index].split(',',1)[0]
        if(valitut[index].split(',',1)[0]==sessionid):
            print "poistettu"
            valitut.remove(valitut[index])


def tb_list_products():

    print "tuotteet"
    for s in products:
        sys.stdout.write(s)


def tb_list_valinnat():

    print "valinnat"
    for s in valinnat:
        sys.stdout.write(s)


def tb_list_valitut():

    print "valitut"
    for s in valitut:
        sys.stdout.write(s)


def tb_haku(hakujono):

    print "pizzojen haku menu:hun"

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
                string = sessionid+","+s
                valinnat.append(string)

    tb_list_valinnat()


def tb_valitut(komentojono):

    print "pizzojen valinta"

    sanat=komentojono.split(' ',10)

    ok=1;
    for s in range(len(sanat)): # 16.9.2016 JariK
        if sanat[s][0]=='+':
            ok=0;

    if ok==1:

        valikko=2
        # This routine goes thru products selected with keywords,
        # and writes products matching index in given by user
        # command line.

        # Go thru all words in command line
        for index in range(len(sanat)):

            # If this word is numeric, find x th product
            # to valitut array.

            if(isnum(sanat[index])):
                c=0 # c has number of line in this session
                d=0 # d has index into array
                e=int(sanat[index]) # e has number user gave
                while True:
                    if(valinnat[d].split(',',1)[0]==sessionid):
                        c=c+1
                    if(c==e):
                        break;
                    d=d+1

                valitut.append(valinnat[d])
    

#    tb_list_valitut()


def tb_lisataytteet(komentojono):

    print "lisataytteet pizzoille"

    sanat=komentojono.split(' ',10)

    ok=0;
    
    # For this part to be run, we need extra toppings
    # in command

    for s in range(len(sanat)): # 16.9.2016 JariK
        if sanat[s][0]=='+':
            ok=1;

    if ok == 1:

        valikko=3
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
                    if(valinnat[d].split(',',1)[0]==sessionid):
#                        print valitut[c]

                        # This line is product

                        if 'pizza' in valitut[c]:
#                            print "valittu"
                            d=d+1
                    c=c+1

#                print "c", c, "d", d, "len valitut 2", len(valitut)

                # Skip toppings

                while(c < len(valitut)):
                    if(valinnat[d].split(',',1)[0]==sessionid):
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
                                string = sessionid+","+t
#                                print "lisätty",string
                                if(c<len(valitut)): # 21.9.2016 JariK
                                    valitut.insert(c,string)
                                else:
                                    valitut.append(string)
                            print t
                        
#    tb_list_valitut()


def tb_command(custline):

    print(custline)

    if(custline==''):
        print "tyhjä"

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

    # Remove spaces in beginning of command
    
    while(len(custline)>0 and custline[0]==' '):
        custline=custline[1:]

    # Remove spaces in end of command

    while(len(custline)>0 and custline[-1]==' '):
        custline=custline[:-1]

    print(custline)

#    print custline.split(' ',1)

    tb_haku(custline)
    tb_valitut(custline)
    tb_lisataytteet(custline)
    for index in range(len(valitut)):
        print valitut[index]

def tb_answer(): # 27.9.2016 JariK 
    global valikko
    print "valikko", valikko
    answer=[]    
    if(valikko==0):

#        for index in range(len(valitut)):
        answer.append(products)
    
    elif(valikko==1):
        answer.append(valinnat)

    elif(valikko==2):
        answer.append(valitut)

    print "anssi"

    return(answer)


print "thebutler"
print 'tuotteiden valinta raaka-aineiden tai nimen mukaan: "kinkku ananas"'
print 'valinta listasta: "2"'
print 'lisätäytteet "1+valkosipuli"'
print 'pizzan valinta ja lisataytteet: "hollywood 1 1+valkosipuli"'

tb_init()

#while(True):
    #custline=raw_input('Enter your input:')
    #if not (custline==''):
        #tb_command(custline)
        #answer=tb_answer(custline)
        #print answer
   #elif(valikko==1):
        #tb_list_products()
        #valikko=(valikko+1) % 3;
    #elif(valikko==2):
        #tb_list_valinnat()
        #valikko=(valikko+1) % 3;
    #elif(valikko==3):
        #tb_list_valitut()
        #valikko=(valikko+1) % 3;sys
