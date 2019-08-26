#29.05.2019 YTJ Module
from bs4 import BeautifulSoup
import DRIVER

def ytjInfoPagePart(page):
    soup = BeautifulSoup(page,'lxml')
    try:
        t=soup.find('tbody')
    except:
        t='error'

    
    return t

def vat(ovt):
    vat=ovt[4:11]+'-'+ovt[-1]
    vat=str(vat).strip()
    return vat

def checkOvt(ovt,page_part):
    if page_part!='error':
        v = vat(ovt)
        tab = page_part.find_all('td')
        Name = list()
        for i in range(len(tab)):
            if v in str(tab[i]):
                Name.append(tab[i+1].string.strip())
                
                return Name
    else:
        return []

def checkName(nazwa, driver):

    d = dict()
    driver = driver
    page = DRIVER.ytj_search(driver,nazwa)
    if page !='error':
        tab = page.find_all('td') ##bylo page_part
        for i in range(len(tab)):
            if name in str(tab[i]):
                newName = tab[i].string.strip()
                d['ytj_company_name']=newName
                d['ytj_error']='OK'
    else:
        d['ytj_company_name']="no name"
        d['ytj_error']='ERROR, ytj web page error'


    return d 

def ytjCheck(driver, ovt, nazwa):
    d = dict()
    driver = driver
    vata = vat(ovt).strip()
    page = DRIVER.ytj_search(driver,vata)

    if page !='error':
        p = ytjInfoPagePart(page)
        n = checkOvt(ovt,p)
        if len(n) == 1:
            
            d['ytj_company_name']=n[0]
            d['ytj_error']='OK'
        elif len(n)>1:
            d['ytj_company_name']=''
            d['ytj_error']='ERROR, to many possibilieties'

    else:
            #po vat nie znajdzie to sprawdzi ewentualnie nazwe
            #d= checkName(nazwa, driver)
            d['ytj_company_name']=''
            d['ytj_error']='ERROR, to many possibilieties'
            

    return d

