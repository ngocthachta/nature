#-*- coding: utf8 -*-

from satis_webapp import login, satis_url
from windtest import create_windtest, windtest_object
from acqsystem import acqsystem, configuration_element
from safin import *
from satisgit.satisgit import git_update_file


import json
import jsonpickle
import logging

logger = logging.getLogger("usermodule")

class user_module_type():
    def __init__(self, deviceType = "InterpreterUserModule", deviceServerName = "InterpreterUserModule",
            deviceClassName = "InterpreterUserModule"):
        self.deviceType = deviceType
        self.deviceServerName = deviceServerName
        self.deviceClassName = deviceClassName

class user_module(acqsystem):
    def __init__(self, windTestId = "", reference = "master", id = None, 
            type = "CorrectedParameter", logicalName = "iumod_1", 
            physicalName = "UserModule", isValid = False, acqSystemType = "UserModuleConfig", 
            userModuleType = user_module_type()):
        acqsystem.__init__(self, windTestId = windTestId, reference = reference, id = id, 
                    type = type, logicalName = logicalName, physicalName = physicalName, 
                    isValid = isValid, acqSystemType = acqSystemType)
        self.userModuleType = userModuleType

    def to_JSON(self):
        json_encode = json.loads(jsonpickle.encode(self, unpicklable = False))
        return json.dumps(json_encode, sort_keys = True, indent = 4)

    @classmethod
    def decode_json(cls, json_encode):
        if "@transportid" in json_encode: del json_encode["@transportid"]
        json_encode["py/object"] = "__main__.user_module"
        json_encode["userModuleType"]["py/object"] = "__main__.user_module_type"

        return jsonpickle.decode(json.dumps(json_encode))

def read_user_module(windtest_id, logicalName):
    result = None
    session = login()
    r = session.get(satis_url + "windtest/%s/reference/master/userModuleConfig/" % windtest_id)
    for usermodule_json in r.json():
        logger.debug("read user_module %s" % json.dumps(usermodule_json, sort_keys = True, indent = 4))
        user_module_obj = user_module.decode_json(usermodule_json)
        if user_module_obj.logicalName == logicalName:
            result = user_module_obj
    return result

def create_user_module(windtest_id, logicalName = "iumod_1", physicalName = "InterpreterUserModule", 
        usmtype = "InterpreterUserModule"):
    user_module_obj = read_user_module(windtest_id, logicalName = logicalName)
    if user_module_obj == None:
        user_module_obj = user_module(logicalName = logicalName, physicalName = physicalName, 
            acqSystemType = "UserModuleConfig", type = "UserModuleConfig")

    user_module_obj.windTestId = windtest_id
    user_module_obj.userModuleType.deviceType = usmtype
    user_module_obj.userModuleType.deviceServerName = usmtype
    user_module_obj.userModuleType.deviceClassNam = usmtype
    session = login()
    r = session.post(satis_url + "windtest/%s/reference/master/userModuleConfig/" % windtest_id, 
            json = json.loads(user_module_obj.to_JSON()))
    user_module_result = user_module.decode_json(r.json())
    logger.debug("user_module obj repondre %s" % user_module_result)

    r = session.get(satis_url + "windtest/%s/reference/master/configurationelement/" %
            windtest_id)
    for configurationelement_json in r.json():
        configurationelement_obj = configuration_element.decode_json(configurationelement_json) 
        if configurationelement_obj.deviceConfigId == user_module_result.id :
            logger.debug("configuration element %s" % configurationelement_obj.to_JSON())
            configurationelement_obj.data = """
# -*- coding: UTF-8 -*-
from gensatisenv import *
# --- veuillez conserver ce bandeau intact svp --- #


#@InterpreterUserModule
# Definition des Variables spécifiques
_unit={}

# Cette 2nd entête ne doit toujours pas être modifié. 
#-------------------------------------#
toto = SafinStationnaire.RAW.M1V1 + 5
            """
            git_update_file(windtest_id, 'calcul/src/user_modules/%s.py' % logicalName, configurationelement_obj.data)
            r = session.post(satis_url + "windtest/%s/reference/master/configurationelement/" % windtest_id,
                    json = json.loads(configurationelement_obj.to_JSON()))

            configurationelement_result = configuration_element.decode_json(r.json())
            logger.debug("configuration element repond %s" % configurationelement_result.to_JSON())

    return user_module_result
    
def main():
    from datetime import datetime
    logger.info("Start configure usermodule")
    
    windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    wt = create_windtest(windtest_id)
    windtest_id = wt.id
    safin_obj = create_safin_stationnaire(windtest_id, logicalName = "SafinStationnaire", physicalName = "F1-SAFIN225",
             nb_module_safin = 16)
    create_user_module(windtest_id, logicalName = "iumod_1", usmtype = "InterpreterUserModule")
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
