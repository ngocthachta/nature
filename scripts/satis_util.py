import requests

import logging
import json
from collections import namedtuple
import os
import jsonpickle
import uuid

logger = logging.getLogger("satis_util")
satis_url = "http://localhost:8081/satis/"

# jsonpickle.load_backend('simplejson')
# jsonpickle.set_preferred_backend('simplejson')
# jsonpickle.set_encoder_options('simplejson', compactly = False, indent = 4)
class windtest():
    def __init__(self, type = '', windTunnel = '', purpose = '', 
            aerNumber = '', testResponsibleName = '', 
            beginDate = None, endDate = None, clientName = '', 
            testClassification = '', description = '', id = '', oldId = ''):
        self.type = type
        self.windTunnel = windTunnel
        self.purpose = purpose
        self.aerNumber = aerNumber
        self.testResponsibleName = testResponsibleName
        self.beginDate = beginDate
        self.endDate = endDate
        self.clientName = clientName
        self.testClassification = testClassification
        self.description = description
        self.id = id
        self.oldId = id

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
                            sort_keys=True, indent=4)

class windtest_object():
     def __init__(self, windTestId = "", reference = "master", id = None, type = "WindTestObject"):
         self.windTestId = windTestId
         self.reference = reference
         self.id = id
         self.type = type

class acqsystem(windtest_object):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "WindTestObject",
            logicalName = "", physicalName = "", isValid = False, acqSystemType = ""):
        windtest_object.__init__(self, windTestId = windTestId, reference = reference, id = id,
                type = type)
        self.logicalName = logicalName
        self.physicalName = physicalName
        self.isValid = isValid
        self.acqSystemType = acqSystemType

class device_config_handled_by_a_clock(acqsystem):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "WindTestObject",
            logicalName = "", physicalName = "", isValid = False, acqSystemType = "", 
            defaultClock = "HDEV", defaultFrequenceRest = 1.0, frameSize = 1000, 
            acquisitionMode = "CONTINUE",
            hsyncDeviceAddress = "",
            usedSynchronizingClock = False):
        acqsystem.__init__(self, windTestId = windTestId, reference = reference, id = id, 
                type = type, logicalName = logicalName, physicalName = physicalName, isValid = isValid, 
                acqSystemType = acqSystemType)
        self.defaultClock = defaultClock
        self.defaultFrequenceRest = defaultFrequenceRest
        self.frameSize = frameSize
        self.acquisitionMode = acquisitionMode
        self.hsyncDeviceAddress = hsyncDeviceAddress
        self.usedSynchronizingClock = usedSynchronizingClock

class sensor():
    def __init__(self, id = "", ref_capteur = "", installationOwner = "", 
            brand = "", type = "", supply = 0.0, supplyUnit = "", physicalUnit = "", 
            sigmaZero = False):
        self.id = id
        self.ref_capteur = ref_capteur
        self.installationOwner = installationOwner
        self.brand = brand
        self.type = type
        self.supply = supply
        self.supplyUnit = supplyUnit
        self.physicalUnit = physicalUnit
        self.sigmaZero = sigmaZero

class channel():
    def __init__(self, parameterName = "", logicalNumber = 0, physicalNumber = 0, designation = "",
            zeroGroup = "", acqSystemType = "", enable= True, sigmaZero = False,
            calibration = None):
        self.parameterName = parameterName
        self.logicalNumber = logicalNumber
        self.physicalNumber = physicalNumber
        self.designation = designation
        self.zeroGroup = zeroGroup
        self.acqSystemType = acqSystemType
        self.enable = enable
        self.sigmaZero = sigmaZero
        self.calibration = calibration

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


class psi8400_unit():
    def __init__(self, id = None, psi8400Config = None, name = "", address = 0):
        self.id = id
        self.psi8400Config = psi8400Config
        self.name = name
        self.address = address

class psi8400_channel_config(channel):
    def __init__(self, parameterName = "", logicalNumber = 0, physicalNumber = 0, designation = "",
            zeroGroup = "", acqSystemType = "PSI8400Config", enable= True, sigmaZero = False,
            calibration = None, psi8400MultiSensorConfig = None, pin = 1, psi8400Config = None):
        channel.__init__(self, parameterName = parameterName, logicalNumber = logicalNumber,
                physicalNumber = physicalNumber, 
                designation = designation, zeroGroup = zeroGroup, acqSystemType = acqSystemType,
                enable= enable, sigmaZero = sigmaZero, calibration = calibration)
        self.psi8400MultiSensorConfig = psi8400MultiSensorConfig
        self.pin = pin
        self.psi8400Config = psi8400Config


class multisensor():
    def __init__(self, id = "", portNumber = 0, spectrum = 5, spectrumUnit = "", 
            brand = "", windTunnelId = "F1", dtc = False, sigmaZero = False):
        self.id = id
        self.portNumber = portNumber
        self.spectrum = spectrum
        self.spectrumUnit = spectrumUnit
        self.brand = brand
        self.windTunnelId = windTunnelId
        self.dtc = dtc
        self.sigmaZero = sigmaZero

class psi8400_multi_sensor_config():
    def __init__(self, id = None, psi8400Config = None, name = "", description = "", 
            multiSensor = None, dauConfig = None, slot = None, thirdSpectrum = False,
            pcuConfig = None, channelConfigList = []):
        self.id = id
        self.psi8400Config = psi8400Config
        self.name = name
        self.description = description
        self.multiSensor = multiSensor
        self.dauConfig = dauConfig
        self.slot = slot
        self.thirdSpectrum = thirdSpectrum
        self.pcuConfig = pcuConfig
        self.channelConfigList = channelConfigList


class psi8400_dau_config(psi8400_unit):
    def __init__(self, id = None, psi8400Config = None, name = "", address = 0, 
            type = "SDU", multiSensorsNumber = 0, multiSensorsNbFr = 8, 
            multiSensorsFrDelay = 0.0, multiSensorConfigList = []):
        psi8400_unit.__init__(self, id = id, psi8400Config = psi8400Config, name = name,
                address = address)
        self.type = type
        self.multiSensorsNumber = multiSensorsNumber
        self.multiSensorsNbFr = multiSensorsNbFr
        self.multiSensorsFrDelay = multiSensorsFrDelay
        self.multiSensorConfigList = multiSensorConfigList

class psi8400_pcu_config(psi8400_unit):
    def __init__(self, id = None, psi8400Config = None, name = "", address = 0,
            mode = "DIFFERENTIAL", unit = "PSI", maxPressureAbsolute = 30.0):
        psi8400_unit.__init__(self, id = id, psi8400Config = psi8400Config, name = name,
                address = address)
        self.mode = mode
        self.unit = unit
        self.maxPressureAbsolute = maxPressureAbsolute

class psi8400(device_config_handled_by_a_clock):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "PSI8400Config",
            logicalName = "", physicalName = "", isValid = False, acqSystemType = "PSI8400Config",
            defaultFrequenceRest = 1.0, frameSize = 1, defaultClock = "HDEV", usedSynchronizingClock = False,
            acquisitionMode = "CONTINUE", hsyncDeviceAddress = "", psi8400DauConfigList = [],
            psi8400PCUConfigList = []):
        device_config_handled_by_a_clock.__init__(self, windTestId = windTestId, reference = reference,
                id = id, type = type, logicalName = logicalName, physicalName = physicalName, 
                isValid = isValid, acqSystemType = acqSystemType, defaultFrequenceRest = defaultFrequenceRest,
                frameSize = frameSize, 
                defaultClock = defaultClock, usedSynchronizingClock = usedSynchronizingClock, 
                acquisitionMode = acquisitionMode, hsyncDeviceAddress = hsyncDeviceAddress)

        self.psi8400DauConfigList = psi8400DauConfigList
        self.psi8400PCUConfigList = psi8400PCUConfigList

    def to_JSON(self):
        json_encode = json.loads(jsonpickle.encode(self, unpicklable = False))

        for jsdau in json_encode["psi8400DauConfigList"]:
            jsdau["psi8400Config"] = None
            for js_multisensor_config in jsdau["multiSensorConfigList"]:
                js_multisensor_config["psi8400Config"] = None
                js_multisensor_config["multiSensor"]["psi8400Config"] = None
                js_multisensor_config["dauConfig"]["psi8400Config"] = None
                uuid_multisensor = str(uuid.uuid1())
                js_multisensor_config["@id"] = uuid_multisensor
                for js_psi_channel in js_multisensor_config["channelConfigList"]:
                    js_psi_channel["psi8400MultiSensorConfig"] = uuid_multisensor

                if js_multisensor_config["pcuConfig"] != None:
                    js_multisensor_config["pcuConfig"]["psi8400Config"] = None

        for jspcu in json_encode["psi8400PCUConfigList"]:
            jspcu["psi8400Config"] = None

        return json.dumps(json_encode, sort_keys = True, indent = 4)

    @classmethod
    def decode_json(cls, json_encode):
        if "@transportid" in json_encode: del json_encode["@transportid"]

        json_encode["py/object"] = "__main__.psi8400"

        for jsdau in json_encode["psi8400DauConfigList"]:
            jsdau["py/object"] = "__main__.psi8400_dau_config"
            for js_multisensor_config in jsdau["multiSensorConfigList"]:
                js_multisensor_config["py/object"] = "__main__.psi8400_multi_sensor_config"
                js_multisensor_config["multiSensor"]["py/object"] = "__main__.multisensor"
                for js_psi_channel in js_multisensor_config["channelConfigList"]:
                    js_psi_channel["py/object"] = "__main__.psi8400_channel_config"

        for jspcu in json_encode["psi8400PCUConfigList"]:
            jspcu["py/object"] = "__main__.psi8400_pcu_config"

        result = jsonpickle.decode(json.dumps(json_encode))

        return result


def create_psi(windtest_id, logicalName = "PSI8400", physicalName = "F1-PSI249"):
    logger.debug("Create psi %s" % physicalName)
    remove_all_psi(windtest_id)
    pcu1 = psi8400_pcu_config(name = "PCU1", address = 113)
    pcu2 = psi8400_pcu_config(name = "PCU2", address = 115)
    dau1 = psi8400_dau_config(name = "DAU1", address = 111, type = "SDU", multiSensorConfigList = [])
    dau2 = psi8400_dau_config(name = "DAU2", address = 112, type = "FIU", multiSensorConfigList = [])

    psi_obj = psi8400(windTestId = windtest_id, logicalName = logicalName,
            physicalName = physicalName, 
            psi8400DauConfigList = [dau1, dau2],
            psi8400PCUConfigList = [pcu1, pcu2])

    psi_obj.defaultClock = "HSYNC"

    session = login() 
    r = session.post(satis_url + "windtest/%s/reference/master/psi8400config"%windtest_id,
            json = json.loads(psi_obj.to_JSON()))

    psi_obj = psi8400.decode_json(r.json())

    dau_config_list = []
    multisensor_config_list = []

    multisensor_id_lst = ["48389", "48390"]

    for indx, multisensor_id in enumerate(multisensor_id_lst):
        indx_i = indx + 1
        multisensor_obj = multisensor(id = multisensor_id)
        lst_channel = []
        for i in range(1, 49):
            psi_channel = psi8400_channel_config(parameterName = "MPSI_%s_M%sC%s"%(indx_i, indx_i, i),
                    pin = i, sigmaZero = True, logicalNumber = indx * 48 + i)
            lst_channel.append(psi_channel)

        multisensor_config = psi8400_multi_sensor_config(multiSensor = multisensor_obj, 
                name = "MPSI_%s" % indx_i, slot = indx_i,
                dauConfig = dau1,
                pcuConfig = pcu1,
                channelConfigList = lst_channel) 

        multisensor_config_list.append(multisensor_config)

    dau_config1 = psi8400_dau_config(id = None, psi8400Config = None, name = "DAU1", 
             address = 111, type = "SDU", 
             multiSensorsNumber = len(multisensor_config_list), 
             multiSensorConfigList = multisensor_config_list)
    dau_config_list.append(dau_config1)

    multisensor_config_list = []
    multisensor_id_lst = ["641114", "641225", "641226", "641227", "641228", "641230",
            "641229", "641231", "641232", "641265", "641266", "641268", "641278", "641305"]

    for indx, multisensor_id in enumerate(multisensor_id_lst):
        indx_i = indx + 3
        multisensor_obj = multisensor(id = multisensor_id)
        lst_channel = []
        for i in range(1, 65):
            psi_channel = psi8400_channel_config(parameterName = "MPSI_%s_M%sC%s"%(indx_i, indx_i, i),
                    pin = i, sigmaZero = True, logicalNumber = 2 * 48 + indx * 64 + i)
            lst_channel.append(psi_channel)

        multisensor_config = psi8400_multi_sensor_config(multiSensor = multisensor_obj, 
                name = "MPSI_%s" % indx_i, slot = indx_i - 2,
                dauConfig = dau2,
                pcuConfig = pcu2,
                channelConfigList = lst_channel) 

        multisensor_config_list.append(multisensor_config)

    dau_config2 = psi8400_dau_config(id = None, psi8400Config = None, name = "DAU2", 
             address = 112, type = "FIU", 
             multiSensorsNumber = len(multisensor_config_list), 
             multiSensorConfigList = multisensor_config_list)

    dau_config_list.append(dau_config2)
    psi_obj.psi8400DauConfigList = dau_config_list

    r = session.post(satis_url + "windtest/%s/reference/master/psi8400config"%windtest_id,
            json = json.loads(psi_obj.to_JSON()))
    logger.debug("reponse %s "% json.dumps(r.json(), sort_keys = True, indent = 4))
    psi_obj = psi8400.decode_json(r.json())
    logger.debug("psi reponse %s" % psi_obj.to_JSON())

def read_psi(windtest_id):
    session = login()
    r = session.get(satis_url + "windtest/%s/reference/master/psi8400config/getlist/" % windtest_id)
    try :
        result = psi8400.decode_json(r.json()[0])
        return result
    except:
        return None

def remove_all_psi(windtest_id):
    session = login()
    r = session.get(satis_url + "windtest/%s/reference/master/psi8400config/getlist/" % windtest_id)
    try :
        for json_psi in r.json():
            result = psi8400.decode_json(json_psi)
            r = session.delete(satis_url + "windtest/%s/reference/master/psi8400config/%s" % (windtest_id, result.id))
            
    except:
        pass

def create_session(user="user", password="password"):
    os.environ['NO_PROXY'] = 'localhost'
    session = requests.Session()
    session.auth = (user, password)
    return session

def login(url="http://localhost:8081/satis/login", user="user", password="password"):
    session = create_session()
    r = session.get(url, auth=(user, password))
    return session

def create_windtest(windtest_id):
    session = login()
    r = session.get(satis_url + "windtest")
    logger.debug("reponse %s" %r.json())
    try :
        wt = windtest(**(r.json()[0]))
        logger.debug("wt %s" %wt.to_JSON())
    except:
        wt = None
    if wt == None:
        wt = windtest(id = windtest_id, windTunnel = 'F1', type='Monomat')
        logger.debug("create windtest %s" % wt.to_JSON())

        r = session.post(satis_url + "windtest", json = json.loads(wt.to_JSON()))
        wt = windtest(**r.json())
        logger.debug("reponse %s" % json.dumps(r.json(), indent = 4))
    logger.debug("object return %s" % wt.to_JSON())
    return wt

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
    for channel_id in range(7):
       safin_obj.safinConfigChannelList[channel_id].sigmaZero = True
       safin_obj.safinConfigChannelList[channel_id].scaleBridgeDestination = True
    
    session = login()
    r = session.post(satis_url + "windtest/%s/reference/master/safinconfig"%windtest_id, 
            json = json.loads(safin_obj.to_JSON()))
    safin_result = safin.decode_json(r.json())

    logger.debug("Safin stationnaire %s" %safin_result.to_JSON())

def create_safin_instationnaire(windtest_id, logicalName = "Safin_Instationnaire", 
        physicalName = "F1-SAFIN171", nb_module_safin = 16):
    logger.debug("Create Safin Instationnaire %s" % physicalName)
    safin_obj = create_safin(windtest_id, logicalName, physicalName, nb_module_safin)
    safin_obj.defaultClock = "HINT"
    safin_obj.freqInt1.fileName = "AC_FC_20kHz_FINT_50kHz_72" 
    safin_obj.freqInt1.id = 224 # id in the table safin_filters

    session = login()
    r = session.post(satis_url + "windtest/%s/reference/master/safinconfig"%windtest_id, 
            json = json.loads(safin_obj.to_JSON()))
    safin_result = safin.decode_json(r.json())

    logger.debug("Safin Instationnaire %s" %safin_result.to_JSON())

def main():
    from datetime import datetime
    logger.info("Start configure satis")
    
    windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    wt = create_windtest(windtest_id)
    windtest_id = wt.id

    create_safin_stationnaire(windtest_id, logicalName = "Safin_0", physicalName = "F1-SAFIN225",
             nb_module_safin = 16)
    create_safin_stationnaire(windtest_id, nb_module_safin = 2)
    create_safin_instationnaire(windtest_id, nb_module_safin = 4)
    create_psi(windtest_id, logicalName = "PSI8400", physicalName = "F1-PSI249")

    #remove_all_psi(windtest_id)
    #psi_obj = read_psi(windtest_id)
    #logger.debug("psi encode json %s" % psi_obj.to_JSON())
    #logger.debug("reponse obj %s" % psi_obj.to_JSON())
    #logger.debug("obj loop %s" % psi_obj.psi8400DauConfigList[0])
    #logger.debug("obj loop %s" % psi_obj.psi8400DauConfigList[0].multiSensorConfigList[0].multiSensor.id)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
