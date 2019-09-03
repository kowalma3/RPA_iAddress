##send report 30.08.2019

##
##this script is creating reporting ticket, assign it to Robot and send report from it and close the ticket

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time
import conf
import json
from datetime import datetime



USR = conf.usr
PWD = conf.pwd
HOST=conf.host

ROBOT = conf.sa_rpa_roger
GROUP = conf.group

COMPANY=conf.company
SERVICE=conf.service
RECIPIENT_LIST=conf.recipients
CALLER=conf.caller
REPORT = conf.reportFile







def logToTicketSystem():
    '''Login to the ticket system using web browser Firefox'''
    driver = webdriver.Firefox()
    host='https://opusflow.service-now.com/'
    driver.get('https://opusflow.service-now.com/login.do')
    elem=driver.find_element_by_id('user_name')
    elem.clear()
    elem.send_keys(USR)
    elem=driver.find_element_by_id('user_password')
    elem.clear()
    elem.send_keys(PWD)
    submit_button = driver.find_elements_by_id('sysverb_login')[0]
    submit_button.click()
    time.sleep(5)

    return driver


def openIncident():
    '''open incdent in ticketing tool using rest api'''

    url = HOST+'/api/now/table/incident'
    headers = {"Content-Type":"application/json","Accept":"application/json"}

        
    data=json.dumps({"assigned_to":ROBOT,
                     "assignment_group":GROUP,
                     "cmdb_ci":SERVICE,
                     "caller_id":CALLER,
                     "company":COMPANY,
                     "u_disable_notification":'true',
                     "short_description":'Roger report',
                     "description":'Report will be send via e-mail'
        })
    response = requests.post(url, auth=(USR,PWD), headers=headers ,data=data)

    # Check for HTTP codes other than 200
    if response.status_code != 201: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        return ERROR

    # Decode the JSON response into a dictionary and use the data
    data = response.json().get('result')
    number=data.get('number')
    sys_id=data.get('sys_id')
    
    return number,sys_id

def sendMessage(driver, sys_id,description):
    '''send message using selenium, because e-mail api dosen't work'''
    url='https://opusflow.service-now.com/email_client.do?sysparm_table=incident&sysparm_sys_id='+sys_id+'&sysparm_target=incident&sys_target=incident&sys_uniqueValue='+sys_id+'&sys_row=0&sysparm_encoded_record=&sysparm_domain_restore=false&sysparm_stack=no'
    driver.get(url)
    time.sleep(5)
    
    elem=driver.find_element_by_xpath('/html/body/div[2]/form/div[1]/div/div/span[1]/span')
    elem.click()
    elem.send_keys(Keys.BACKSPACE)

    elem=driver.find_element_by_id('sys_display.to_block')
    elem.clear()
    elem.send_keys(RECIPIENT_LIST)

    elem=driver.find_element_by_id('sys_display.cc_block')
    elem.clear()
    elem.send_keys('Tiina.Astren@opuscapita.com')

    driver.switch_to.frame(driver.find_element_by_id('message.text_ifr'))
    elem=driver.find_element_by_xpath('//*[@id="tinymce"]')
    elem.clear()
    elem.send_keys(description)
    driver.switch_to.default_content()
    
    elem=driver.find_element_by_id('send_button')
    elem.click()
    time.sleep(5)

    driver.close()
    driver.quit()

def close(sys_id):
    url = 'https://opusflow.service-now.com/api/now/table/incident/'+str(sys_id)


    headers = {"Content-Type":"application/json","Accept":"application/json"}
	 
    response = requests.put(url, auth=(USR,PWD), headers=headers ,data='{"close_notes":"closed","subcategory":"Human error","state":"6"}')
		 
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

def create_report():
    data = ''
    with open(REPORT,'r') as f:
        data = f.read()
        
    report = ''
    data = data.split('\n')
    currentHouer = datetime.today().strftime('%H')
    print(currentHouer)
    currentDate = datetime.today().strftime('%Y-%m-%d')
    if currentHouer == '12':
        l = ['08','09','10','11']
        for H in l:
            
            for line in data:
                if currentDate+' '+H in line:
                    report = report + line +'\n'

    elif currentHouer == '15':
        l= ['12','13','14','15']
        for H in l:
            print(currentDate+' '+ H )
            for line in data:
                if currentDate+' '+H in line:
                    report = report + line +'\n'

    return report                
def create_message():
    report = create_report()

    if report:
        report = report
    else:
        report = 'None'

    message = '''Hi,
    today I have done following requests: \n''' + report +'''

    with kind regards,
    Roger the Robot ;)'''

    return message

def main():
    inc,sys_id = openIncident()

    message = create_message()
    print(message)
    time.sleep(30)

    if inc !='ERROR':
        driver = logToTicketSystem()
        sendMessage(driver, sys_id,message)
        close(sys_id)

main()




    
    




    



