#30.07.2019
#Main Flow

###Tieto dodac/skopiowac!! dzis!!!

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
import check_if_proper_site_is_loaded

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
            if 'TE' in element['electronic_adr']:           ###tieto operator!!!! drugi w ChangeExisting.py a trzeci a AddNew.py
                adr = element['electronic_adr'][2:]
            else:
                adr = element['electronic_adr']
            d.update({'electronic_adr':adr})
            d.update({'lmc':element['lmc']})

    d.update({'number':ticket['number']})
    d.update({'sys_id':ticket['sys_id']})
    d.update({'operator':ticket['operator']})
    d.update({'date':ticket['date']})
    d.update({'busines_id':ticket['busines_id']}) #company receiving id
    d.update({'address_tbc':ticket['address_tbc']}) #company electronic address

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
def addNew(driver,element):
    print('adding new:') #usun
    print(element) #usun
    potwierdzenie = input("is it correct? y/n ")#usun
    if potwierdzenie == 'y': #usun
        
        link = AddNew.addNewOrg(driver,element.get('ytj_name'),element.get('number'))
        #operator = operator_number(element.get('operator'))
        operator = element.get('operator')
        AddNew.addNewSite(driver,link,operator,element.get('busines_id'),element.get('address_tbc'),element.get('number'))
        time.sleep(10)
        ##zalogowac
        OF.informCustomer(element['sys_id'],'1')
        log.add_log(element['sys_id']+':'+element['number']+':'+'New routing has been added, close complete')
        OF.close(element['sys_id'],'1',3)
        print('closed')
        
        #OF.returnToCS(element['sys_id'],'New routing has been added,customer informed, scenario1') ##zamienic na close complete
        ##oddac do CS/ponformowac klienta
def allDisabledAdd(driver, element):
    print('all disabled check org_link before accept!!!!! should be tested:') #usun
    print(element) #usun
    potwierdzenie = input("is it correct? y/n ")
    if potwierdzenie == 'y':
        for element in allDisabled:
            addSite.addNewSite(driver,element.get('org_link'),element.get('operator'),element.get('address_tbc'),element.get('number')) ### na org link mo¿e siê wywalic, trzeba sprawdzic
            time.sleep(10)
            log.add_log(element['sys_id']+':'+element['number']+':'+'Routing has been added')
            OF.returnToCS(element['sys_id'],'Routing has been changed, please inform customer')

def change(driver,element):

    print('change existing, please check') #usun
    print(element) #usun
    potwierdzenie = input("is it correct? y/n ")
    if potwierdzenie == 'y':
        
            
        #decyzja o dacie
        if_date = data(element.get('date'))

        if if_date:
            data_ = zmodyfikuj_date(element.get('date'))
        else:
            data_=''

        if element.get('electronic_adr') == element.get('address_tbc') and element.get('lmc')== OPERATORS.op.get(element.get('operator')):
            log.add_log(element['sys_id']+':'+element['number']+':'+'Routing exist, close complete')
            #OF.informCustomer(element['sys_id'],'1')
            OF.close(element['sys_id'],'1',3)
            print('closed')
            #OF.returnToCS(element['sys_id'],'Routing exist, customer informed, please check')
        else:
            odp = ChangeExisting.changeSite(driver,element.get('site_link'),element.get('operator'),element.get('address_tbc'),data_,element.get('number'))
            time.sleep(10)
            if odp == 'OK':
                log.add_log(element['sys_id']+':'+element['number']+':'+'Routing has been changed, close complete')
                OF.informCustomer(element['sys_id'],'1')
                OF.close(element['sys_id'],'1',3)
                print('closed')
                #OF.returnToCS(element['sys_id'],'Routing has been changed, customer informed')
            elif odp == 'ERROR':
                log.add_log(element['sys_id']+':'+element['number']+':'+'2 Receiving Identifiers return to CS for improvement')
                OF.returnToCS(element['sys_id'],'2 Receiving Identifiers please check',0)
    
def mainFlow():

    driver = DRIVER.start()

    lista = OF.getCasesFromQueue() #create list of tasks
    print('ile tixow w kolejce'+str(len(lista)))

    #####tu dodam

    #check_if_proper_site_is_loaded.check(driver,lista)

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

    print('ilosc tixow przed ytj check:'+str(len(main_lista)))

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
            OF.informCustomer(ticket['sys_id'],'2') #inform customer
            OF.returnToCS(ticket['sys_id'],ytj_d.get('ytj_error','')+' - inform customer, scenario 2',8) ##inform customer and send back to CS as awaiting customer
            log.add_log(ticket['sys_id']+':'+ticket['number']+':'+ytj_d.get('ytj_error','')+':customer informed - scenario 2, ticket send to CS')
            temp.remove(ticket)

    main_lista=temp
    print('ilosc tixow po ytj check:'+str(len(main_lista)))
      ###iAddress validation, and actions
      ###return to CS if OC routing, 2 enables, exist as requested
      ###create "Add new" list of dictionaries
      ###create "change existing" list of dict
      ###create "all disabled" list of dictionaries

    DRIVER.logToiAddress(driver)
    for ticket in main_lista:
        print('next ticket')
        potwierdzenie = input("is it correct? y/n ")
        if potwierdzenie == 'y':
            ##zmiana logiki sprawdz iAddress i podejmij decyzje.Wszystkie tixy powinny sie lapac teraz
            #pobieram dane z iAddressu
            bi = ticket.get('busines_id','')
            bi.strip(' ')
            l=IADDRESS_Module.getData(bi,driver)
            if 'opus' in ticket.get('operator').lower():

                ###########OC w tixie, co robić? OC in IAddress, routing exist, other case return to CS, 'Operator is OpusCapita , operator can't be changed' 
                ########w przyszlosci sprobuj zmienic na powyzsze
                #OF.returnToCS(ticket['sys_id'],'Operator is OpusCapita , operator can\'t be changed') ##podmien na close
                OF.informCustomer(ticket['sys_id'],'4')
                OF.close(ticket['sys_id'],'4',4)
                
                log.add_log(ticket['sys_id']+':'+ticket['number']+':'+'Operator is OpusCapita , operator can\'t be changed, close incomplete')
            if l == '':
                #nie ma wpisow w iAdress, dodaj nowy wpis
                addNew(driver,ticket)
            elif ocRouting(l):
                #OC Routing
                #OF.informCustomer(ticket['sys_id'],'4')
                #OF.returnToCS(ticket['sys_id'],'OC routing enabled, scenario 4, customer informed') ##podmien na close
                OF.close(ticket['sys_id'],'4',4)
                log.add_log(ticket['sys_id']+':'+ticket['number']+':'+'OC routing enabled,close incomplete')
            elif twoRoutings(l) == 2: ####tu zostal dodany kod
                #>%
                exist = False
                for element in l:
                    if 'enable' in element['status'].lower():
                        #print(element['electronic_adr'],ticket['address_tbc'] , element['lmc'], ticket['operator'])
                        if (element['electronic_adr'] == ticket['address_tbc'] )and (element['lmc'] in ticket['operator']):
                            print('tuuuuu')
                            #time.sleep(30)
                            log.add_log(ticket['sys_id']+':'+ticket['number']+':'+'Routing exist, 2 routings, close complete')
                            #OF.informCustomer(element['sys_id'],'1')
                            OF.close(ticket['sys_id'],'1',3)
                               
                            exist=True
                #%<
                if not exist:
                    OF.returnToCS(ticket['sys_id'],'2 routing enabled, please check',0) ##poten przesylac do klienta
                    log.add_log(ticket['sys_id']+':'+ticket['number']+':'+'2 routing enabled')
            elif twoRoutings(l) == 0:
                ##wszystko disabled
                d=dict()
                d=ticket
                d.update({'org_link':l[0].get('org_link','')})
                allDisabledAdd(driver,d)
            else:
                d = dict()
                d= getData(l,ticket)
                if d:
                    change(driver,d)
    driver.close()
    driver.quit()
###wywolanie,
    
if __name__ == '__main__':
    mainFlow()
