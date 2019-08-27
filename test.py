import DRIVER, AddNew

import OPERATORS,iAddressOperators

from bs4 import BeautifulSoup


driver = DRIVER.start()
DRIVER.logToiAddress(driver)

driver.get('https://iaddress.itella.net/eivc-ui/hd/site-edit.htm?siteId=629233')

page = driver.page_source

soup = BeautifulSoup(page,'lxml')


t = soup.find('table',id='siteIdentifiersTable')

rows = t.find_all('tr')

print(len(rows))

#
#link = AddNew.addNewOrg(driver, 'test1_kowalma3', 'OCRT12345')
##link='https://iaddress.itella.net/eivc-ui/hd/organization-edit.htm?orgId=557402'
###print(link)
#####funkcja na wyluskanie operatora
##
##op = OPERATORS.op.get('Apix Messaging Oy (003723327487)','')
##
##operator = iAddressOperators.op.get(op,'')
##
##if operator:
##    AddNew.addNewSite(driver,link,'Apix Messaging Oy (003723327487)','007719999999999','007799999999991','OCRT12345')
##    #AddNew.addNewSite(driver,link, operator,'007719999999999','007799999999991' 'OCRT12345')
##
