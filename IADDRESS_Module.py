#11.06.2019 IADDRESS Module
from bs4 import BeautifulSoup
import DRIVER

def existInIAddress(page): ##tu sprawdzanie czy istnieje czy nie
    soup = BeautifulSoup(page,'lxml')
    t= soup.find_all(class_="even")
    if len(t)>0:
        return t
    else:
        return 'error'


def getData(companyElectronicAddress,driver):
    page = DRIVER.getDataFromIAddress(driver,companyElectronicAddress)
    t = existInIAddress(page)
    lista=list()
    if t!='error':
        for element in t:
            d=dict()
            w= element.find_all('td')
            
            d.update({'org_link':w[0].find('a').get('href')})
            d.update({'site_link':w[1].find('a').get('href')})
            d.update({'site_id':w[2].contents[2].strip(' \n\t')})
            d.update({'electronic_adr':w[3].contents[2].strip(' \n\t')})
            d.update({'lmc':w[5].find('b').contents[0].strip(' \n\t')})
            d.update({'status':w[6].contents[0].strip(' \n\t')})

            lista.append(d)
    else:
        #lista.append('empty iaddress')
        return ''
    return lista
        
    
