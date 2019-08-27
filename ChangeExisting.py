##12.07
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import OPERATORS
import OP
def getXpath(driver):
    xpath=''
    soup = BeautifulSoup(driver.page_source,'lxml')
    t = soup.find_all('tbody')
    tabela = t[5].find_all('tr')
    for i, element in enumerate(tabela,start=1):
        a=element.find(class_="receiveChannelsChange recChannelStatus")
        if 'bs4' in str(type(a)):
            b = a.find(selected="selected")
            if 'Enabled'== b.string:
                xpath = '/html/body/div/div[3]/div[2]/div/div[1]/table[2]/tbody/tr['+str(i)+']'

    return xpath


def checkIdentifiersNumber(page):
    soup = BeautifulSoup(page,'lxml')


    t = soup.find('table',id='siteIdentifiersTable')

    rows = t.find_all('tr')

    return(len(rows))

def changeSite(driver, siteId, operator, electronic_address ,date,ticket): ##
    oper=operator
    operator = OPERATORS.op.get(oper)


    
    driver.get("https://iaddress.itella.net/eivc-ui/hd/"+siteId)
    time.sleep(5)
    page = driver.page_source
    ##check how many identyfiers 2019-08-27
    if(checkIdentifiersNumber(page)>2):
        #oddaj do CS z notka
        return ERROR
    #search for one enabled, to at the end disable it

    path = getXpath(driver)
    e_for_disablibg=''
    if path :
        e_for_disablibg= driver.find_element_by_xpath(path+'/td[3]/select')
    e = driver.find_element_by_class_name('addSiteReceiveChannel')
    e.click()
    ###basic add site, without date
    e = driver.find_element_by_id('lmc')
    select = Select(e)
    select.select_by_visible_text(operator)
    e = driver.find_element_by_id('electronicAddress')
    e.send_keys(electronic_address)


    if date:
        e=driver.find_element_by_id('effectiveStart')
        e.click()
        time.sleep(1)
        e.click()
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(date)
        e.send_keys('0')
        e.send_keys('0')
        time.sleep(3)
        e= driver.find_element_by_xpath(path+'/td[9]/input[2]')
        e.click()
        time.sleep(1)
        e.click()
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        e.send_keys(date)
        e.send_keys('0')
        e.send_keys('0')
    ##disable prevoius enabled
    else:
        select = Select(e_for_disablibg)
        select.select_by_visible_text('Disabled')

    element = driver.find_element_by_id('operationTicketId')
    element.send_keys(ticket)

    element = driver.find_element_by_id('operationComment')
    element.send_keys(ticket)

    e= driver.find_element_by_id('saveSite')
    e.click()

    e = driver.find_element_by_id('popup_ok')
    e.click()

    time.sleep(2)
    return 'OK'
