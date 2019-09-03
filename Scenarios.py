#4 scenarios
#messages module
#messages description
###1-	a)Totally new routing has been added (either basic or scheduled)
##  -	b)Existing routing has been changed (either basic or scheduled)
##  -	c)Valid routing exists already, no changes.
##Request is set to Closed Complete status by the robot.


###2-    There is a mismatch with company name and OVT compared to data in YTJ (robot wil check the business ID in YTJ). 
## -     Robot will send a message to customer to check and confirm the company information.
## -     Request is set to Awaiting customer status and assigned to CS FI Customer Service.


###3-There is a mismatch in Operator that customer is requesting and what is currently available in Verkkolaskuosoite.fi.
##This does not apply to cases when routing is via OpusCapita (see scenario 4)
##Robot will send a message to customer to check and confirm the Operator information.
##Request is set to Awaiting customer status and assigned to CS FI Customer Service.


###4-There is an existing routing via OpusCapita.
##Robot will send a message to customer that we are not able to make the requested change and will close the request without any actions.
##Request is set to Closed incomplete status.

#### 5,6,7,8 - action return to CS with info
#5- caller nordea
#6- description not empty
#7- sh-description check
#8- attachments exists

messages={
    '1':'''Hei,
Reitityksenne on tarkistettu / lisätty / ajastettu, voitte alkaa lähettämään verkkolaskuja kyseiselle yritykselle heti tai kun pyytämänne poikkeava aloituspäivä astuu voimaan.

Your routing request is checked / added / scheduled, you can start sending electronic invoices to the requested Company immediately or after the requested date take effect.
 ''',
    '2':'''Hei,
Antamanne yritystiedot eivät näytä täsmäävän. Tarkistatteko yrityksen virallisen nimen ja OVT-tunnuksen ja ilmoittakaa tarkistetut tiedot meille vastaamalla tähän sähköpostiin, kiitos!
Yrityksen virallisen nimen voitte tarkistaa täältä : https://www.ytj.fi/
OVT-tunnuksen voitte tarkistaa täältä: https://verkkolaskuosoite.fi/client/index.html

There seem to be mismatch with the Company name to be routed and Company Receiving ID. Please check the company details and inform us by replying to this message.
Official company name can be checked from: https://www.ytj.fi/
Company Receiving ID can be checked from: https://verkkolaskuosoite.fi/client/index.html
 ''',
    '3':'''Hei,
Verkkolaskuosoite.fi sivuston (https://verkkolaskuosoite.fi/client/index.html) mukaan yrityksellä näyttää olevan voimassaoleva reititys toisen operaattorin kautta. Tarkistatteko operaattoritiedon asiakkaaltanne ja ilmoittakaa tarkistetut tiedot meille vastaamalla tähän sähköpostiin, kiitos!

According to Verkkolaskuosoite.fi page (https://verkkolaskuosoite.fi/client/index.html), there seems to be an existing routing via another operator. Please check the operator information from your customer and inform us by replying to this message.

 ''',
    '4':'''Hei,
Yrityksellä on voimassaoleva reititys OpusCapitan kautta. Emme voi tehdä pyydettyä muutosta, ennen kuin nykyinen reititys on irtisanottu. Suljemme tämän työpyynnön ilman toimenpiteitä ja pyydämme teitä tekemään meille uuden pyynnön, kun asiakkaanne on irtisanonut voimassaolevan reitityksen.

Please note that there is an existing routing via OpusCapita. We are unable to make the requested change until the current routing has been terminated. This request will be closed without any actions.
Please send us a new request when the existing routing has been terminated.
 ''',
	'5':'''Hi, 
	Caller is from Nordea company.
 ''',
	'6':'''Hi,
	More information field is not empty
 ''',
	'7':'''Hi,
	if it not request for new B2B e-invoice routing to iAddress
 ''',
    }
