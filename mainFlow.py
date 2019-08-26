#30.07.2019
#Main Flow

###Tieto dodac/skopiowac!!

import OF #opusflow module, a set of functions to communication with opusflow.
import log
import DRIVER
import YTJ_Module
import IADDRESS_Module
import OPERATORS, iAddressOperators
import time
import datetime
import ChangeExisting
import AddNew

def data(date):
    now = datetime.datetime.now()

    month = int(date[5:7])
    day = int(date[8:10])

    if now.month == month:
        if now.day - day < -1:
            return True
        else:
            return False
    elif now.month > month:
        return False
    elif now.month < month:
        return True

def zmodyfikuj_date(data):
       t= data.split('-')
       new_data= t[2]+'.'+t[1]+'.'+t[0]+' 00:00'
       return new_data



def operator_number(op):

    temp = OPERATORS.op.get(op,'')
    nr = iAddressOperators.op.get(temp,'')

    return nr


def getData(l, ticket):

    d = dict()

    for element in l:
        if 'enable' in element['status'].lower():
            d.update({'site_link':element['site_link']})
            d.update({'electronic_adr':element['electronic_adr']})
            d.update({'lmc':element['lmc']})

    d.update({'number':ticket['number']})
    d.update({'sys_id':ticket['sys_id']})
    d.update({'operator':ticket['operator']})
    d.update({'date':ticket['date']})
    d.update({'busines_id':ticket['busines_id']})
    d.update({'address_tbc':ticket['address_tbc']})

    return d
 ######stare nowe, co na co zmieniamy, dokonczyc jesli czegos zabraknie
def ocRouting(l):
    for element in l:
        if ('BEL' in element['lmc'] or 'BEL' in element['electronic_adr']) and 'enable' in element['status'].lower():
            return True

    return False

def twoRoutings(l):

    n=0

    for element in l:
        if 'enable' in element['status'].lower():
            n=n+1

    if n > 1:
        return 2
    elif n==1:
        return 1
    elif n==0:
        return 0

def mainFlow():

    driver = DRIVER.start()

    lista = OF.getCasesFromQueue() #create list of tasks

    if lista:

        temp = OF.checkLogs(lista) #check remove previously processed task
        lista = temp
    else:
        print('no tasks in queue exit program')
        #exit() ##no tasks in queue exit program, czy to potrzebne?



    ###buduje liste slownikow do dalszej analizy
    ###tu tez moze byc oddany task do cs, z informacja
    ###albo zamkniety z infrmacja dla klienta, musi to byc zalogowane
    ###w tym momencie odbywa sie tez walidacja danych z taska
    main_lista=list()

    for ticket in lista:

        temp = OF.getDataFromTask(ticket)
        if temp!='ERROR':
            main_lista.append(temp)

    ###ytj validation
    ###jak problem z nazwa, oddaj narazie do CS z informacja i usun z listy

    temp = main_lista

    for ticket in main_lista:
        cn = ticket.get('company_name','')
        bi = ticket.get('busines_id','')
        bi.strip(' ')
        if bi :

            ytj_d = YTJ_Module.ytjCheck(driver,bi, cn)

        error = ytj_d.get('ytj_error','')

        if error == 'OK':
            ticket.update({'ytj_name':ytj_d.get('ytj_company_name','')})
        else:

            OF.returnToCS(ticket['sys_id'],ytj_d.get('ytj_error','')+' - please inform customer') ##tu zmienic na oddawanie klientowi
            log.add_log(ticket['sys_id']+':'+ticket['number']+':'+ytj_d.get('ytj_error',''))
            temp.remove(ticket)

    main_lista=temp
      ###iAddress validation, and actions
      ###return to CS if OC routing, 2 enables, exist as requested
      ###create "Add new" list of dictionaries
      ###create "change existing" list of dict
      ###create "all disabled" list of dictionaries

    addNew=list()
    changeExisting=list()
    allDisabled=list()

    DRIVER.logToiAddress(driver)

    temp=main_lista

    for ticket in main_lista:
        bi = ticket.get('busines_id','')
        bi.strip(' ')

        l=IADDRESS_Module.getData(bi,driver)

        if l == '':
                d=dict()
                d = ticket
                addNew.append(d)
                temp.remove(ticket)
                continue

        if ocRouting(l):
                OF.returnToCS(ticket['sys_id'],'OC routing enabled') ##poten przesylac do klienta
                log.add_log(ticket['sys_id']+':'+ticket['number']+':'+'OC routing enabled')
                temp.remove(ticket)
                continue

        numberOfEnabled = twoRoutings(l) ##count number of enabled routings
        if numberOfEnabled == 2:
                OF.returnToCS(ticket['sys_id'],'2 routing enabled') ##poten przesylac do klienta
                log.add_log(ticket['sys_id']+':'+ticket['number']+':'+'2 routing enabled')
                temp.remove(ticket)
                continue
        if numberOfEnabled == 0:
                ###co potrzebne mi przy dodawaniu nowego situ ?
                d=dict()
                d=ticket
                d.update({'org_link':l[0].get('org_link','')})
                allDisabled.append(d)
                temp.remove(ticket)
                continue

        d = dict()
        d= getData(l,ticket)
        if d:
                changeExisting.append(d)
                temp.remove(ticket)
                continue
            ###na koncu sprawdz co nigdzie nie wpadlo.


    main_lista = temp

    print("\n\n kompletnie nowe\n")
    print(addNew)
    if addNew:
        potwierdzenie = input("is it correct? y/n ")
        if potwierdzenie == 'y':

            ####funkcja w petli
            for element in addNew:
                link = AddNew.addNewOrg(driver,element.get('ytj_name'),element.get('number'))
                operator = operator_number(element.get('operator'))
                AddNew.addNewSite(driver,link,operator,element.get('busines_id'), element.get('number'))
                time.sleep(10)
                ##zalogowac
                log.add_log(element['sys_id']+':'+element['number']+':'+'New routing has been added')
                OF.returnToCS(element['sys_id'],'New routing has been added, please inform customer')
                ##oddac do CS/ponformowac klienta



    print("\n\n do zmiany \n\n")
    print(changeExisting)

    if changeExisting:
        potwierdzenie = input("is it correct? y/n ")
        if potwierdzenie == 'y':
            for element in changeExisting:
                ##porownanie operatorow i addresow, czy w ogole wchodzic w funkcje, jak nie to wyjsc z logiem odpowiednim
                ##rozbicie, zmien operator, zmien address, zmien operator i adress z data??

                #decyzja o dacie
                if_date = data(element.get('date'))

                if if_date:
                    data_ = zmodyfikuj_date(element.get('date'))
                else:
                    data_=''

                if element.get('electronic_adr') == element.get('address_tbc') and element.get('lmc')== OPERATORS.op.get(element.get('operator')):
                    log.add_log(element['sys_id']+':'+element['number']+':'+'Routing exist')
                    OF.returnToCS(element['sys_id'],'Routing exist')
                    continue

                ChangeExisting.changeSite(driver,element.get('site_link'),element.get('operator'),element.get('address_tbc'),data_,element.get('number'))
                time.sleep(10)
                log.add_log(element['sys_id']+':'+element['number']+':'+'Routing has been changed')
                OF.returnToCS(element['sys_id'],'Routing has been changed, please inform customer')

    print("\n\n wszystko disabled \n\n")
    print(allDisabled)

    if allDisabled:
        potwierdzenie = input("is it correct? y/n ")
        if potwierdzenie == 'y':
            for element in allDisabled:
                addSite.addNewSite(driver,element.get('site_link'),element.get('operator'),element.get('address_tbc'),element.get('number'))
                time.sleep(10)
                log.add_log(element['sys_id']+':'+element['number']+':'+'Routing has been added')
                OF.returnToCS(element['sys_id'],'Routing has been changed, please inform customer')

    print("\n\nbez akcji \n\n") #oddac do CS
    print(main_lista)

    if main_lista:
        log.add_log(element['sys_id']+':'+element['number']+':'+'No acction has been recognized')
        OF.returnToCS(element['sys_id'],'No acction has been recognized, please check')



mainFlow()
