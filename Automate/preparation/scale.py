from satis_webapp import login, satis_url
from windtest import create_windtest, windtest_object
from acqsystem import channel, device_config_handled_by_a_clock, sensor, acqsystem
from safin import *
from definition.test_utils import updateDbCoeffBalance

import json
import jsonpickle
import logging

logger = logging.getLogger("scale")

class corrected_parameter(windtest_object):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "CorrectedParameter", 
            acqSystemId = None, unit = "mV", dataLevel = "RAW", parameterName = "", 
            description = "", tangoAddress = "", dimension = 0, isFromCalculDevice = False):
        windtest_object.__init__(self, windTestId = windTestId, reference = reference, id = id,
                type = type)
        self.acqSystemId = acqSystemId
        self.unit = unit
        self.dataLevel = dataLevel
        self.parameterName = parameterName
        self.description = description
        self.tangoAddress = tangoAddress
        self.dimension = dimension
        self.isFromCalculDevice = isFromCalculDevice

class scale(acqsystem):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "ScaleConfig",
            logicalName = "Balance_0", physicalName = "BalanceMonomat", isValid = False, 
            acqSystemType = "ScaleConfig", scaleName = "PHI190-02", calibrationId = None,
            xd = corrected_parameter(), xl = corrected_parameter(), m1 = corrected_parameter(),
            m2 = corrected_parameter(), n1 = corrected_parameter(), n2 = corrected_parameter(), 
            l = corrected_parameter(),  attackAngle = corrected_parameter(), 
            sideSlipAngle = corrected_parameter()):
        acqsystem.__init__(self, windTestId = windTestId, reference = reference, id = id, 
                    type = type, logicalName = logicalName, physicalName = physicalName, isValid = isValid, 
                acqSystemType = acqSystemType)
        self.scaleName = scaleName
        self.calibrationId = calibrationId
        self.xd = xd
        self.xl = xl
        self.m1 = m1
        self.m2 = m2
        self.n1 = n1
        self.n2 = n2
        self.l = l
        self.attackAngle = attackAngle
        self.sideSlipAngle = sideSlipAngle
    def to_JSON(self):
        json_encode = json.loads(jsonpickle.encode(self, unpicklable = False))
        return json.dumps(json_encode, sort_keys = True, indent = 4)
    
    @classmethod
    def decode_json(cls, json_encode):
        if "@transportid" in json_encode: del json_encode["@transportid"]
        json_encode["py/object"] = "__main__.scale"
        if "xd" in json_encode and json_encode["xd"] != None:
            json_encode["xd"]["py/object"] = "__main__.corrected_parameter"
        if "xl" in json_encode and json_encode["xl"] != None:
            json_encode["xl"]["py/object"] = "__main__.corrected_parameter"
        if "m1" in json_encode and json_encode["m1"] != None:
            json_encode["m1"]["py/object"] = "__main__.corrected_parameter"
        if "m2" in json_encode and json_encode["m2"] != None:
            json_encode["m2"]["py/object"] = "__main__.corrected_parameter"

        if "n1" in json_encode and json_encode["n1"] != None:
            json_encode["n1"]["py/object"] = "__main__.corrected_parameter"
        if "n2" in json_encode and json_encode["n2"] != None:
            json_encode["n2"]["py/object"] = "__main__.corrected_parameter"
        if "l" in json_encode and json_encode["l"] != None:
            json_encode["l"]["py/object"] = "__main__.corrected_parameter"
        if "attackAngle" in json_encode and json_encode["attackAngle"] != None:
            json_encode["attackAngle"]["py/object"] = "__main__.corrected_parameter"
        if "sideSlipAngle" in json_encode and json_encode["sideSlipAngle"] != None:
            json_encode["sideSlipAngle"]["py/object"] = "__main__.corrected_parameter"

        return jsonpickle.decode(json.dumps(json_encode))

def read_scale(windtest_id, scaleLogicalName):
    result = None
    session = login()
    r = session.get(satis_url + "windtest/%s/reference/master/scaleconfig/getlist/" % windtest_id)
    
    for scale_json in r.json():
        logger.debug("read scaleconfig %s" % json.dumps(scale_json, sort_keys = True, indent=4))
        scale_obj = scale.decode_json(scale_json)
        if scale_obj.logicalName == scaleLogicalName:
            result = scale_obj
    return result

def create_scale(windtest_id, logicalName = "Balance_0", physicalName = "PHI190-02", safin_obj = None):
    scale_obj = read_scale(windtest_id, logicalName)
    if scale_obj == None:
        scale_obj = scale()

    scale_obj.logicalName = logicalName
    scale_obj.physicalName = physicalName
    scale_obj.scaleName = physicalName
    scale_obj.address = "tango/balance/PHI190-02"
    scale_obj.calibrationId = 2380

    scale_obj.xd.acqSystemId = safin_obj.id
    scale_obj.xd.parameterName = "XD"
    scale_obj.xd.groupTangoAddress = "%s/MOD1_RAWVALUES[0]" % safin_obj.address

    scale_obj.m1.acqSystemId = safin_obj.id
    scale_obj.m1.parameterName = "M1"
    scale_obj.m1.groupTangoAddress = "%s/MOD1_RAWVALUES[1]" % safin_obj.address

    scale_obj.m2.acqSystemId = safin_obj.id
    scale_obj.m2.parameterName = "M2"
    scale_obj.m2.groupTangoAddress = "%s/MOD1_RAWVALUES[2]" % safin_obj.address

    scale_obj.n1.acqSystemId = safin_obj.id
    scale_obj.n1.parameterName = "N1"
    scale_obj.n1.groupTangoAddress = "%s/MOD1_RAWVALUES[3]" % safin_obj.address

    scale_obj.n2.acqSystemId = safin_obj.id
    scale_obj.n2.parameterName = "N2"
    scale_obj.n2.groupTangoAddress = "%s/MOD1_RAWVALUES[4]" % safin_obj.address

    scale_obj.l.acqSystemId = safin_obj.id
    scale_obj.l.parameterName = "L"
    scale_obj.l.groupTangoAddress = "%s/MOD1_RAWVALUES[5]" % safin_obj.address

    scale_obj.xl.acqSystemId = safin_obj.id
    scale_obj.xl.parameterName = "XL"
    scale_obj.xl.groupTangoAddress = "%s/MOD1_RAWVALUES[6]" % safin_obj.address

    scale_obj.attackAngle.acqSystemId = safin_obj.id
    scale_obj.attackAngle.dataLevel = "ENG"
    scale_obj.attackAngle.parameterName = "CLINO"
    scale_obj.attackAngle.groupTangoAddress = "%s/MOD1_ENGVALUES[7]" % safin_obj.address

    scale_obj.sideSlipAngle.acqSystemId = safin_obj.id
    scale_obj.sideSlipAngle.dataLevel = "ENG"
    scale_obj.sideSlipAngle.parameterName = "POTTOUR"
    scale_obj.sideSlipAngle.groupTangoAddress = "%s/MOD2_ENGVALUES[0]" % safin_obj.address

    session = login()
    r = session.post(satis_url + "windtest/%s/reference/master/scaleconfig" % windtest_id,
            json = json.loads(scale_obj.to_JSON()))
    scale_obj = scale.decode_json(r.json())
    logger.debug("scale %s" % scale_obj.to_JSON())

    updateDbCoeffBalance(physicalName, windtest_id)

def main():
    from datetime import datetime
    logger.info("Start configure satis")
    
    windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    wt = create_windtest(windtest_id)
    windtest_id = wt.id
    safin_obj = create_safin_stationnaire(windtest_id, logicalName = "SafinStationnaire", physicalName = "F1-SAFIN225",
             nb_module_safin = 16)

    create_scale(windtest_id, logicalName = "BalanceMonomat", physicalName = "PHI190-02", safin_obj = safin_obj)

    # scale_obj = read_scale(windtest_id, "Balance_0")
    # logger.debug("scale %s" % scale_obj)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
