##12.07
def getXpath(driver):
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




def changeSite(driver, siteId, operator, address ,date,ticket): ##
    driver.get("https://iaddress.itella.net/eivc-ui/hd/site-edit.htm?siteId="+siteId)
    time.sleep(5)
    #search for one enabled, to at the end disable it

    path = getXpath(driver)
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
        e.driver.find_element_by_id('effectiveStart')
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
