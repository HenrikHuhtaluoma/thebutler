import sys

fileid=open("/var/thebutler/thebutler.dat","r")
productlines=fileid.readlines()
sessionid="123456"
valitut=[]
print "init done"

def testi():
    print "testimaarittely"
	
def tb_setsessionid(sessionid2):
    sessionid=sessionid2
    print sessionid

def isnum(value):
    try:
        int(value)
        return True
    except:
        return False

def tb_haku(hakujono):
    c=1;
    sanat=hakujono.split(' ',10)
    for s in productlines:
        ok=1;
        for index in range(len(sanat)):
            if not isnum(sanat[index]):
                if sanat[index] not in s:
                    ok=0;
        
        if(ok==1):
            sys.stdout.write(str(c)+". ")
            sys.stdout.write(s)
            c+=1
            string = sessionid+","+s
            valitut.append(string)

def tb_valitut(komentojono):

    sanat=komentojono.split(' ',10)
    for index in range(len(sanat)):
        if(isnum(sanat[index])):
            print sanat[index]
            c=0
            d=0
            e=int(sanat[index])
            while(c<e):
                print valitut[d].split(',',1)[0]
                if(valitut[d].split(',',1)[0]==sessionid):
                  c=c+1
                d=d+1
            print valitut[d]
            
#tb_setsessionid("1234")
#while(True):
    #custline=raw_input('Enter your input:')
    #print(custline)
    #print custline.split(' ',1)
    #tb_haku(custline)
    #tb_valitut(custline)
