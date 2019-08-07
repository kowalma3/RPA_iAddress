#driver module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#import iAddressOperators
import time
import conf
from bs4 import BeautifulSoup

def start():
    driver =webdriver.Firefox()
    return driver

def end(driver):
    driver.quit()

def load_page(driver,url):
    driver.get(url)
    time.sleep(5)


def page(driver):
    return driver.page_source

def ytj_search(driver,name):
    load_page(driver,'https://ytj.fi')
    e=driver.find_element_by_id('search-term')
    e.clear()
    try:
        e.send_keys(name)
        e.send_keys(Keys.ENTER)
        time.sleep(5)
        return driver.page_source
    except:
        return 'error'

def logToiAddress(driver):
    driver.get("https://iaddress.itella.net/eivc-ui/hd/login.htm")
    e = driver.find_element_by_id('username')
    e.clear()
    e.send_keys(conf.IAusr)
    e1  = driver.find_element_by_id('password')
    e1.clear()
    e1.send_keys(conf.IApwd)
    e3 = driver.find_element_by_id('submitLogin')
    e3.click()

def getDataFromIAddress(driver,companyElectronicAddress):
    e = driver.find_element_by_id('id')####was search is now
    e.clear()
    e.send_keys(companyElectronicAddress.strip()+'*')#companyElectronicAddress ??
    e = driver.find_element_by_id('idType')
    select = Select(e)
    select.select_by_visible_text('eDIRA')
    
    driver.find_element_by_id("searchSubmit").click()
    time.sleep(10)
    try:
        return driver.page_source
    except:
        return 'error'

def getXpath(driver):
    soup = BeautifulSoup(driver.page_source,'lxml')
    t = soup.find_all('tbody')
    tabela = t[5].find_all('tr')
    for i, element in enumerate(tabela,start=1):
        a=element.find(class_="receiveChannelsChange recChannelStatus")
        if 'bs4' in str(type(a)):
            b = a.find(selected="selected")
            if 'Enabled'== b.string:
                xpath = '/html/body/div/div[3]/div[2]/div/div[1]/table[2]/tbody/tr['+str(i)+']/td[3]/select'

    return xpath

    

    
def changeSite(driver,siteId, operator, electronic_address,date): ##
    driver.get("https://iaddress.itella.net/eivc-ui/hd/site-edit.htm?siteId="+siteId)
    time.sleep(5)
    #search for one enabled, to at the end disable it
    
    path = getXpath(driver)
    if path :
        e_for_disablibg= driver.find_element_by_xpath(path) 
    e = driver.find_element_by_class_name('addSiteReceiveChannel')
    e.click()
    ###basic add site, without date
    e = driver.find_element_by_id('lmc')
    select = Select(e)
    select.select_by_visible_text(operator)
    e = driver.find_element_by_id('electronicAddress')
    e.send_keys(electronic_address)

    ##disable prevoius enabled
    try:
        select = Select(e_for_disablibg)
        select.select_by_visible_text('Disabled')
    except:
        print('nic nie zmieniam')
    
    

    
