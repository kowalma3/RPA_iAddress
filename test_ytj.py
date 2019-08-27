#ytj test

import YTJ_Module
import DRIVER

driver =DRIVER.start()
ovt='003724880180'
nazwa='RS-Insinöörit Oy'

print(YTJ_Module.ytjCheck(driver,ovt,nazwa))
