from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from time import sleep
import OF
from datetime import datetime

log=''
def addToErrorLog(ytj, iaddress):
    today = datetime.today().strftime('%Y%m%d')
    with open('ErrorLog.txt','w+') as f:
        f.write(str(today)+':'+'ytj:'+ytj+', iaddress: '+iaddress+'\n')
        
def checkErrorLog():
    today = datetime.today().strftime('%Y%m%d')
    number = 0
    with open('ErrorLog.txt','r') as f:
        for line in f:
            if today in line:
                number = number + 1

    return number

def checkYtjPage(driver):
    driver.get('https://ytj.fi')
    page = driver.page_source
    soup = BeautifulSoup(page,'lxml')

    l = soup.find_all('p')

    if l:
        for element in l:
            for e in element.contents:
                if 'Teemme muutostöitä YTJ-järjestelmässä. Pahoittelemme katkosta mahdollisesti aiheutuvaa haittaa' in e:
                    return 'ERROR'
        return 'OK'
    else:
        return 'ERROR'

    
def checkIaddressPage(driver):
    driver.get('https://iaddress.itella.net/eivc-ui/hd/login.htm')

    page = driver.page_source

    soup = BeautifulSoup(page,'lxml')

    l = soup.find_all('input')

    if l:
        return 'OK'
    else:
        return 'ERROR'



def check(driver, list_of_tasks):
    ytj = checkYtjPage(driver)
    iaddress = checkIaddressPage(driver)
    
    if ytj == 'OK' and iaddress == 'OK':
        return 'OK'
    else:

        addToErrorLog(ytj,iaddress)
        n = checkErrorLog()

        if n > 3:
            log = 'ytj.fi site: '+ytj+', and iaddress is : '+iaddress+'. It was checked 3 times. Please resend this task to Roger when the system works again.'
            for ticket in list_of_tasks:
                OF.returnToCS(ticket, log,0)

            exit()
        else:
            ##work notes and awaiting 3rd party
            log = 'Error with web page. ytj.fi site: '+ytj+', and iaddress is : '+iaddress
            for ticket in list_of_tasks:
                OF.changeStatusAndAddWorknotes(ticket,log,'-6')
            exit()
        




