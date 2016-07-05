from satis_webapp import satis_url, login
from acqsystem import channel, device_config_handled_by_a_clock, sensor
from windtest import create_windtest

import logging
import json
import jsonpickle

logger = logging.getLogger("safin")

class safin_config_channel(channel):
    def __init__(self, parameterName = "", logicalNumber = 0, physicalNumber = 0, designation = "",
            zeroGroup = "", acqSystemType = "SafinConfig", enable= True, sigmaZero = False,
            safinConfig = None, moduleNumber = 0, advance = 0, 
            gain = 1000, sensor = None, scaleBridgeDestination = False, calibration = None):
        channel.__init__(self, parameterName = parameterName, logicalNumber = logicalNumber,
                physicalNumber = physicalNumber, 
                designation = designation, zeroGroup = zeroGroup, acqSystemType = acqSystemType,
                enable= enable, sigmaZero = sigmaZero, calibration = calibration)
        self.safinConfig = safinConfig
        self.moduleNumber = moduleNumber
        self.advance = advance
        self.gain = gain
        self.sensor = sensor
        self.scaleBridgeDestination = scaleBridgeDestination

class safin_config_module():
    def __init__(self, id = None, safinConfig = None, moduleNumber = 0, mode = "", 
            filterType = "FINT1"):
        self.id = id
        self.safinConfig = safinConfig
        self.moduleNumber = moduleNumber
        self.mode = mode
        self.filterType = filterType

class reference_type():
    def __init__(self, dataModelName = "safin_filters", name = "FILTER", ordinal = 1):
        self.dataModelName = dataModelName
        self.name = name
        self.ordinal = ordinal

class filter():
    def __init__(self, id = 222, fileName = "DC_PasseTout", clockMode = "HINT", 
            referenceType = None):
        self.id = id
        self.fileName = fileName
        self.clockMode = clockMode
        self.referenceType = reference_type()

class safin(device_config_handled_by_a_clock):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "SafinConfig",
            logicalName = "", physicalName = "", isValid = False, acqSystemType = "SafinConfig",
            defaultFrequenceRest = 1.0, frameSize = 1, defaultClock = "HDEV", usedSynchronizingClock = False,
            acquisitionMode = "CONTINUE",
            hsyncDeviceAddress = "", freqInt1 = None, freqInt2 = None, 
            freqExt1 = None, freqExt2 = None, freqExt3 = None, freqExt4 = None,
            freqExt5 = None, freqExt6 = None, freqExt7 = None, freqExt8 = None,
            safinConfigChannelList = [], safinConfigModuleList = []):
        device_config_handled_by_a_clock.__init__(self, windTestId = windTestId, reference = reference,
                id = id, type = type, logicalName = logicalName, physicalName = physicalName, 
                isValid = isValid, acqSystemType = acqSystemType, defaultFrequenceRest = defaultFrequenceRest,
                frameSize = frameSize, 
                defaultClock = defaultClock, usedSynchronizingClock = usedSynchronizingClock, 
                acquisitionMode = acquisitionMode, hsyncDeviceAddress = hsyncDeviceAddress)
        self.freqInt1 = freqInt1
        self.freqInt2 = freqInt2
        self.freqExt1 = freqExt1
        self.freqExt2 = freqExt2
        self.freqExt3 = freqExt3
        self.freqExt4 = freqExt4
        self.freqExt5 = freqExt5
        self.freqExt6 = freqExt6
        self.freqExt7 = freqExt7
        self.freqExt8 = freqExt8
        self.safinConfigChannelList = safinConfigChannelList
        self.safinConfigModuleList = safinConfigModuleList
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
                            sort_keys=True, indent=4)

    @classmethod
    def decode_json(cls, json_encode):
        if "@transportid" in json_encode: del json_encode["@transportid"]

        for jsmod in json_encode["safinConfigModuleList"]:
            jsmod["py/object"] = "__main__.safin_config_module"
            #jsmod["safinConfig"] = json_encode["id"]
            jsmod["safinConfig"] = None 

        for jschannel in json_encode["safinConfigChannelList"]:
            jschannel["py/object"] = "__main__.safin_config_channel"
            jschannel["safinConfig"] = None
            if jschannel["sensor"] != None:
                jschannel["sensor"]["py/object"] = "__main__.sensor"

        json_encode["freqInt1"]["py/object"] = "__main__.filter"
        json_encode["freqInt1"]["referenceType"] = None
        json_encode["py/object"] = "__main__.safin"
        result = jsonpickle.decode(json.dumps(json_encode))
        #result.freqInt1.referenceType = reference_type()
        #result.freqInt1.referenceType = None

        return result

def read_safin(windtest_id, safinLogicalName):
    session = login()
    r = session.get(satis_url + "windtest/%s/reference/master/safinconfig/name/%s/get/" % (windtest_id, safinLogicalName))
    logger.debug("read safin %s" % r)
    try :
        result = safin.decode_json(r.json())
        return result
    except :
        return None

def create_safin(windtest_id, logicalName = "Safin_0", physicalName = "F1-SAFIN171",
        nb_module_safin = 16):
    logger.debug("Add safin into windtest")
    safin_obj = read_safin(windtest_id, logicalName)

    session = login()
    if safin_obj == None:
        safin_obj = safin(id = None, windTestId = windtest_id, 
            logicalName = logicalName, physicalName = physicalName)

        # add a new safin first
        r = session.post(satis_url + "windtest/%s/reference/master/safinconfig"%windtest_id, 
                json = json.loads(safin_obj.to_JSON()))
        safin_result = safin.decode_json(r.json())
    else :
        safin_result = safin_obj

    # then update safin with number correct of module
    nb_module = len(safin_result.safinConfigModuleList)
    nb_module_to_add = nb_module_safin - nb_module
    nb_channel_to_add = nb_module_to_add * 8

    for i in range(1, nb_module_to_add + 1):
        module = safin_config_module(moduleNumber = nb_module + i)
        safin_result.safinConfigModuleList.append(module)
    for i in range(1, nb_channel_to_add + 1):
        moduleNumber = i / 8 if i % 8 == 0 else i/8 + 1
        moduleNumber = moduleNumber + nb_module 
        logicalNumber = nb_module * 8  + i
        physicalNumber = i % 8 + 1
        parameterName = "M%sV%s" % (moduleNumber, physicalNumber)
        channel = safin_config_channel(moduleNumber = moduleNumber, 
                logicalNumber = logicalNumber, physicalNumber = physicalNumber, 
                parameterName = parameterName)
        safin_result.safinConfigChannelList.append(channel)

    r = session.post(satis_url + "windtest/%s/reference/master/safinconfig"%windtest_id, 
            json = json.loads(safin_result.to_JSON()))

    safin_result = safin.decode_json(r.json())
    return safin_result

def create_safin_stationnaire(windtest_id, logicalName = "Safin_Stationnaire", 
        physicalName = "F1-SAFIN226", nb_module_safin = 16):
    logger.debug("Create Safin Stationnaire F1-SAFIN171")
    sensor_104350 = sensor(id = "104350@F1", ref_capteur = "104350", brand = "DRUCK",
            type = "PDCR22", supply = 12.0, supplyUnit = "V", physicalUnit = "Pa",
            sigmaZero = True, installationOwner = "F1")
    safin_obj = create_safin(windtest_id, logicalName, physicalName, nb_module_safin)
    safin_obj.freqInt1.fileName = "DC_FC_10Hz_FINT_100Hz_1420ms"
    safin_obj.freqInt1.id = 225 #id in the table safin_filters

    safin_obj.defaultClock = "HSYNC"
    safin_obj.safinConfigChannelList[0].parameterName = "XD"
    safin_obj.safinConfigChannelList[0].sensor = sensor_104350
    safin_obj.safinConfigChannelList[0].sigmaZero = True

    safin_obj.safinConfigChannelList[1].parameterName = "M1"
    safin_obj.safinConfigChannelList[1].sensor = sensor_104350
    safin_obj.safinConfigChannelList[1].sigmaZero = True

    safin_obj.safinConfigChannelList[2].parameterName = "M2"
    safin_obj.safinConfigChannelList[2].sensor = sensor_104350
    safin_obj.safinConfigChannelList[2].sigmaZero = True

    safin_obj.safinConfigChannelList[3].parameterName = "N1"
    safin_obj.safinConfigChannelList[3].sensor = sensor_104350
    safin_obj.safinConfigChannelList[3].sigmaZero = True

    safin_obj.safinConfigChannelList[4].parameterName = "N2"
    safin_obj.safinConfigChannelList[4].sensor = sensor_104350
    safin_obj.safinConfigChannelList[4].sigmaZero = True

    safin_obj.safinConfigChannelList[5].parameterName = "L"
    safin_obj.safinConfigChannelList[5].sensor = sensor_104350
    safin_obj.safinConfigChannelList[5].sigmaZero = True

    safin_obj.safinConfigChannelList[6].parameterName = "XL"
    safin_obj.safinConfigChannelList[6].sensor = sensor_104350
    safin_obj.safinConfigChannelList[6].sigmaZero = True

    safin_obj.safinConfigChannelList[7].parameterName = "CLINO"
    safin_obj.safinConfigChannelList[7].sensor = sensor_104350
    safin_obj.safinConfigChannelList[7].sigmaZero = True

    safin_obj.safinConfigChannelList[8].parameterName = "POTTOUR"
    safin_obj.safinConfigChannelList[8].sensor = sensor_104350
    safin_obj.safinConfigChannelList[8].sigmaZero = True

    safin_obj.safinConfigChannelList[9].parameterName = "DPREF1"
    safin_obj.safinConfigChannelList[9].sensor = sensor_104350
    safin_obj.safinConfigChannelList[9].sigmaZero = True

    safin_obj.safinConfigChannelList[10].parameterName = "DPREF2"
    safin_obj.safinConfigChannelList[10].sensor = sensor_104350
    safin_obj.safinConfigChannelList[10].sigmaZero = True

    safin_obj.safinConfigChannelList[11].parameterName = "CONTMAX"
    safin_obj.safinConfigChannelList[11].sensor = sensor_104350
    safin_obj.safinConfigChannelList[11].sigmaZero = True
    for channel_id in range(7):
       safin_obj.safinConfigChannelList[channel_id].sigmaZero = True
       safin_obj.safinConfigChannelList[channel_id].scaleBridgeDestination = True
    
    session = login()
    r = session.post(satis_url + "windtest/%s/reference/master/safinconfig"%windtest_id, 
            json = json.loads(safin_obj.to_JSON()))
    safin_result = safin.decode_json(r.json())

    logger.debug("Safin stationnaire %s" %safin_result.to_JSON())
    return safin_result

def create_safin_instationnaire(windtest_id, logicalName = "Safin_Instationnaire", 
        physicalName = "F1-SAFIN171", nb_module_safin = 16):
    logger.debug("Create Safin Instationnaire %s" % physicalName)
    sensor_104350 = sensor(id = "104350@F1", ref_capteur = "104350", brand = "DRUCK",
            type = "PDCR22", supply = 12.0, supplyUnit = "V", physicalUnit = "Pa",
            sigmaZero = True, installationOwner = "F1")
    safin_obj = create_safin(windtest_id, logicalName, physicalName, nb_module_safin)
    safin_obj.defaultClock = "HINT"
    safin_obj.freqInt1.fileName = "AC_FC_10kHz_FINT_5kHz" 
    safin_obj.freqInt1.id = 34 # id in the table safin_filters

    safin_obj.safinConfigChannelList[0].parameterName = "XD"
    safin_obj.safinConfigChannelList[0].sensor = sensor_104350
    safin_obj.safinConfigChannelList[0].sigmaZero = True

    safin_obj.safinConfigChannelList[1].parameterName = "M1"
    safin_obj.safinConfigChannelList[1].sensor = sensor_104350
    safin_obj.safinConfigChannelList[1].sigmaZero = True

    safin_obj.safinConfigChannelList[2].parameterName = "M2"
    safin_obj.safinConfigChannelList[2].sensor = sensor_104350
    safin_obj.safinConfigChannelList[2].sigmaZero = True

    safin_obj.safinConfigChannelList[3].parameterName = "N1"
    safin_obj.safinConfigChannelList[3].sensor = sensor_104350
    safin_obj.safinConfigChannelList[3].sigmaZero = True

    safin_obj.safinConfigChannelList[4].parameterName = "N2"
    safin_obj.safinConfigChannelList[4].sensor = sensor_104350
    safin_obj.safinConfigChannelList[4].sigmaZero = True

    safin_obj.safinConfigChannelList[5].parameterName = "L"
    safin_obj.safinConfigChannelList[5].sensor = sensor_104350
    safin_obj.safinConfigChannelList[5].sigmaZero = True

    safin_obj.safinConfigChannelList[6].parameterName = "XL"
    safin_obj.safinConfigChannelList[6].sensor = sensor_104350
    safin_obj.safinConfigChannelList[6].sigmaZero = True

    safin_obj.safinConfigChannelList[7].parameterName = "CLINO"
    safin_obj.safinConfigChannelList[7].sensor = sensor_104350
    safin_obj.safinConfigChannelList[7].sigmaZero = True

    safin_obj.safinConfigChannelList[8].parameterName = "POTTOUR"
    safin_obj.safinConfigChannelList[8].sensor = sensor_104350
    safin_obj.safinConfigChannelList[8].sigmaZero = True

    safin_obj.safinConfigChannelList[9].parameterName = "DPREF1"
    safin_obj.safinConfigChannelList[9].sensor = sensor_104350
    safin_obj.safinConfigChannelList[9].sigmaZero = True

    safin_obj.safinConfigChannelList[10].parameterName = "DPREF2"
    safin_obj.safinConfigChannelList[10].sensor = sensor_104350
    safin_obj.safinConfigChannelList[10].sigmaZero = True

    safin_obj.safinConfigChannelList[11].parameterName = "CONTMAX"
    safin_obj.safinConfigChannelList[11].sensor = sensor_104350
    safin_obj.safinConfigChannelList[11].sigmaZero = True
    for channel_id in range(7):
       safin_obj.safinConfigChannelList[channel_id].sigmaZero = True
       safin_obj.safinConfigChannelList[channel_id].scaleBridgeDestination = True


    session = login()
    r = session.post(satis_url + "windtest/%s/reference/master/safinconfig"%windtest_id, 
            json = json.loads(safin_obj.to_JSON()))
    safin_result = safin.decode_json(r.json())

    logger.debug("Safin Instationnaire %s" %safin_result.to_JSON())
    return safin_result

def main():
    from datetime import datetime
    logger.info("Start configure satis")
    
    windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    wt = create_windtest(windtest_id)
    windtest_id = wt.id
    create_safin_stationnaire(windtest_id, logicalName = "SafinStationnaire", physicalName = "F1-SAFIN225",
             nb_module_safin = 16)
    create_safin_instationnaire(windtest_id, logicalName = "SafinDynamique", nb_module_safin = 4)
  
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
