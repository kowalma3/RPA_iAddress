import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import OPERATORS

def addNewSite(driver,siteId, operator,electronic_address, ticket):

    ## w org_link podmien 'organization-edit' na 'site-create'
    link = "https://iaddress.itella.net/eivc-ui/hd/site-edit.htm?siteId="+siteId
    driver.get(link)

    e= driver.find_element_by_class_name('addSiteReceiveChannel')
    e.click()
    time.sleep(1)

    e=driver.find_element_by_id('lmc')

    select = Select(e)   ##????


    oper = OPERATORS.op.get(operator)
    operator = oper

      
    select.select_by_visible_text(operator) 
    
    e=driver.find_element_by_id('electronicAddress')

    e.send_keys(electronic_address)
    e.click()
    time.sleep(1)
    e=driver.find_element_by_id('operationTicketId')
    e.send_keys(ticket)
    e=driver.find_element_by_id('operationComment')
    e.send_keys(ticket)

    e= driver.find_element_by_id('saveNewSite')
    e.click()
    time.sleep(1)
    e = driver.find_element_by_id('popup_ok')
    e.click()

    time.sleep(2)
    print('done')
