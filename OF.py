#OF
import conf
import log
import OPERATORS, iAddressOperators

import requests, json


#####Glob variables

HOST = conf.host
OFUSER = conf.ofusr
OFPWD = conf.ofpwd


CS_GROUP = conf.OC_CS_FI_Customer_Service
ROBOT_GROUP = conf.OC_CS_FI_Customer_Service_Robots

ROGER = conf.sa_rpa_roger


def assignToRoger(sys_id):

    url = HOST+'/api/now/table/sc_req_item/'+sys_id
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    d = {'assigned_to':ROGER}

    dane = json.dumps(d)

    response = requests.put(url, auth=(OFUSER, OFPWD), headers=headers ,data=dane)

    if response.status_code != 200: 
        return 'ERROR'

    
def returnToCS(sys_id, message): #simple return, if case was already processed, or not B2B request

    
    url = HOST+'/api/now/table/sc_req_item/'+sys_id
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    work_notes=message

    d={"assignment_group":CS_GROUP,"work_notes":work_notes}
    dane = json.dumps(d)

    response = requests.put(url, auth=(OFUSER, OFPWD), headers=headers ,data=dane)

    if response.status_code != 200: 
        return 'ERROR'
    
def getDataFromOpusFlow(url):
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    response=requests.get(url, auth=(OFUSER, OFPWD), headers=headers)
    
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        return ''
    return response.json()


def getCasesFromQueue(): #build list of tasks to be processed, first validation, if it is B2B request. If yes add to list, if not 
    url = HOST+'/api/now/table/task?sysparm_query='+'assignment_group='+ROBOT_GROUP+'^stateIN-6,1,2^numberSTARTSWITHOCRITM^short_descriptionLIKEiAddress' ###check URL
    response = getDataFromOpusFlow(url)
    lista = list()

    if response !='':
        temp = response.get('result',None)
        if temp :
            for element in temp:
                if "Request for new B2B e-invoice routing to iAddress" in element.get('short_description'):
                    lista.append(element.get('sys_id',None))
                    assignToRoger(element.get('sys_id',None))
                else:
                    #oddaj do CS, z informacja, ze to nie jest
                    message = returnToCS(element.get('sys_id',None),'Based on short description, this is not B2B routing request')
                    if message == 'ERROR':
                        #zaloguj ze nie mozesz oddac do CS, a to nie jest request B2B
                        log.add_log(element.get('sys_id',None)+':'+element.get('number',None)+':: this is not B2B reques, problem with returning it to CS')
        return lista
    else:
        return lista



def checkLogs(lista):

    temp=lista

    for element in lista:

        if log.exists(element):
            returnToCS(element,'This request was already processed, please check it.')
            temp.remove(element)
    lista=temp

    return lista

def nuberOfAttachment(sys_id):
    
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    url=HOST+'/api/now/table/sys_attachment?sysparm_query=table_sys_id%3D'+sys_id
    response = requests.get(url, auth=(OFUSER, OFPWD), headers=headers )  

    lista = response.json().get('result','')

    if lista:

        return 1
         
    else:
        return 0


def checkOperator(operator):
    if 'opus' not in operator.lower():
        temp = OPERATORS.op.get(operator,'')
        if temp !='':
            return True
        else:
            return False
    else:
        return False


def getDataFromTask(sys_id):
    url=HOST+'/sc_req_item.do?JSONv2&sysparm_action=getRecords&sysparm_query=sys_id='+sys_id+'&displayvariables=true'
    response = getDataFromOpusFlow(url)

    if response !='':
        var = response['records'][0].get('variables','')
        if var !='':
            l = dict() ###gdzie robic walidacje ?

            ##get and validate caller
            caller = response['records'][0].get('sys_created_by','')
            if caller != '' and 'nordea'  not in caller.lower():

                l.update({'caller':caller})#caller
            else:
                
                log.add_log(sys_id+'::ERROR, caller Nordea')
                returnToCS(sys_id,'Nordea caller')
                return 'ERROR'
            
            ##add task number and sys_id
            l.update({'number':response['records'][0].get('number','')})#ticket number
            l.update({'sys_id':sys_id})#sys_id

            ##check attachments

            if nuberOfAttachment(sys_id) == 1:
                log.add_log(sys_id+'::ERROR, some attachments')
                returnToCS(sys_id,'Task contains attachments')
                return 'ERROR'

            ##check country

            country = var[0].get('value','')
            if country.lower() == 'finland':
                l.update({'country':country}) #country Finland
            else:
                log.add_log(sys_id+'::ERROR, it is not form for Finland')
                returnToCS(sys_id,'Other than Finish form was choosen.')
                return 'ERROR'
                                
            l.update({'company_name':var[2].get('value','')}) #company name
            l.update({'edira':var[4].get('value','')}) #edira
            l.update({'busines_id':var[7].get('value','')}) #business id
            l.update({'address_tbc':var[8].get('value','')}) #address to be changed

            ##get operator
            operator = var[10].get('value','')
            if operator.lower() == 'other':
                operator = var[12].get('value','')

            ##check operator on the list
            
            if checkOperator(operator):
                l.update({'operator':operator})
            else:
                log.add_log(sys_id+'::ERROR, operator not correct, or OC operator')
                returnToCS(sys_id,'Operator is not on the list or OC is the operator, please check')
                return 'ERROR'
            
##            l.update({'operator':var[10].get('value','')})#operator , will be OTHER
##            l.update({'other_operator':var[12].get('value','')})#other operator

            l.update({'date':var[13].get('value','')})#date

            more_info = var[14].get('value','')
            if more_info:
                log.add_log(sys_id+'::ERROR, some additional information in more_info field')
                returnToCS(sys_id,'Additional information from customer')
                return 'ERROR'
            
            
            return l
        else:
            log.add_log(sys_id+'::ERROR, data could not be taken from variables , empty variables')
            returnToCS(sys_id,'Problem with takeing data from this ticket, empty variables as if this is not B2B task, please check.')
            return 'ERROR' 

    else:
        log.add_log(sys_id+'::ERROR, data could not be taken from variables')
        returnToCS(sys_id,'Problem with takeing data from this ticket, please check.')
        return 'ERROR'
