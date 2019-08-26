import DRIVER, AddNew

import OPERATORS,iAddressOperators


driver = DRIVER.start()
DRIVER.logToiAddress(driver)

#link = AddNew.addNewOrg(driver, 'test1_kowalma3', 'OCRT12345')
link='https://iaddress.itella.net/eivc-ui/hd/organization-edit.htm?orgId=557402'
#print(link)
###funkcja na wyluskanie operatora

op = OPERATORS.op.get('Apix Messaging Oy (003723327487)','')

operator = iAddressOperators.op.get(op,'')

if operator:
    AddNew.addNewSite(driver,link, operator,'007799999999999', 'OCRT12345')
