from satis_webapp import satis_url, login
from windtest import create_windtest
from acqsystem import acqsystem

import jsonpickle
import json
import logging

logger = logging.getLogger("genericdevice")

class generic_device(acqsystem):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "GenericDevice",
            logicalName = "Barometre_1", physicalName = "F1-BARO50", isValid = False, 
            acqSystemType = "GenericDevice", address = "", genericDeviceType = "BAROMETERS"):
        acqsystem.__init__(self, windTestId = windTestId, reference = reference, id = id, 
                    type = type, logicalName = logicalName, physicalName = physicalName, isValid = isValid, 
                acqSystemType = acqSystemType, address = address)
        self.genericDeviceType = genericDeviceType

    def to_JSON(self):
        json_encode = json.loads(jsonpickle.encode(self, unpicklable = False))
        return json.dumps(json_encode, sort_keys = True, indent = 4)

    @classmethod
    def decode_json(cls, json_encode):
        if "@transportid" in json_encode: del json_encode["@transportid"]
        json_encode["py/object"] = "__main__.generic_device"

        return jsonpickle.decode(json.dumps(json_encode))

def read_generic_device(windtest_id, logicalName = "Barometre"):
    result = None
    session = login()
    r = session.get(satis_url + "windtest/%s/reference/master/generic" % windtest_id)
    logger.debug("read generic device %s" % r.json())

    for gd_json in r.json():
        gd_obj = generic_device.decode_json(gd_json)
        logger.debug("generic device obj %s" % gd_obj.logicalName)
        if gd_obj.logicalName == logicalName:
            result = gd_obj

    return result

def create_barometre(windtest_id, logicalName = "Barometre", physicalName = "F1-BARO50"):
    barometre_obj = read_generic_device(windtest_id, logicalName)
    if barometre_obj == None:
        barometre_obj = generic_device(logicalName = logicalName, \
                physicalName = physicalName)
    session = login()
    r = session.post(satis_url + "windtest/%s/reference/master/deviceconfig" % windtest_id,
            json = json.loads(barometre_obj.to_JSON()))
    barometre_obj = generic_device.decode_json(r.json())
    logger.debug("barometre %s" % barometre_obj.to_JSON())

def main():
    from datetime import datetime
    logger.info("Start configure generic device")
    
    windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    windtest_id = "Test_MORPHO_F1Plus_2016_R8"
    wt = create_windtest(windtest_id)
    windtest_id = wt.id
    logger.debug("Windtest Id %s" % windtest_id)
    create_barometre(windtest_id, logicalName = "Barometre_1", \
            physicalName = "F1-BARO50")
  
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
