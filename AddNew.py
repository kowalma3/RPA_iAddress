##12.07.2019
##add totaly new organization and site

###needed data:
## organization  = ytj_name
## ticket
##operator from Iaddress list
##Electronic address
##date check i zamiana na format = dd.mm.yyyy 00:00

import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import OPERATORS
def addNewOrg(driver, name, ticket):
    link = 'https://iaddress.itella.net/eivc-ui/hd/organization-create.htm'

    driver.get(link)

    element = driver.find_element_by_name('orgName')
    element.clear()
    element.send_keys(name)

    element = driver.find_element_by_id('operationTicketId')
    element.clear()
    element.send_keys(ticket)

    element = driver.find_element_by_id('operationComment')
    element.clear()
    element.send_keys(ticket)

    element = driver.find_element_by_id('saveNewOrganization')

    element.click()

    element = driver.find_element_by_id('popup_ok')
    element.click()

    time.sleep(5)
    

    return driver.current_url

def addNewSite(driver,org_link, operator,receiving, el_address,ticket):

    ## w org_link podmien 'organization-edit' na 'site-create'
    'https://iaddress.itella.net/eivc-ui/hd/site-create.htm?orgId=563279'
    link = org_link.replace('organization-edit','site-create')
    driver.get(link)

    ###receiving id add  on the top 27-08-2019
    time.sleep(10)
    e = driver.find_element_by_class_name('addSiteIdentifier')
    e.click()
    time.sleep(5)
    e= driver.find_element_by_xpath('//*[@id="siteIdentifiersTable"]/tbody/tr/td/input[@type="text"]')
    
    time.sleep(1)
    e.send_keys(receiving)
    
    time.sleep(20)

    e= driver.find_element_by_class_name('addSiteReceiveChannel')
    e.click()
    time.sleep(1)

    e=driver.find_element_by_id('lmc')

    select = Select(e)   ##????

    oper = OPERATORS.op.get(operator)
    operator = oper

    print(operator)
    
    select.select_by_visible_text(operator) #lista operatorow albo już bedzie dory numer podany np '75', albo trzeba tu wybrac


    e=driver.find_element_by_id('electronicAddress')

    e.send_keys(el_address)
    e.click()
    e=driver.find_element_by_id('operationTicketId')
    e.send_keys(ticket)
    e=driver.find_element_by_id('operationComment')
    e.send_keys(ticket)
    time.sleep(2)
    e= driver.find_element_by_id('saveNewSite')
    e.click()
    time.sleep(2)
    e = driver.find_element_by_id('popup_ok')
    e.click()

    time.sleep(2)
    print('done')
    ###przetestuj i dodaj akceptacje
