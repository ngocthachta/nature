from satis_webapp import login, satis_url
from windtest import create_windtest
from acqsystem import channel, device_config_handled_by_a_clock, sensor

import json
import jsonpickle
import logging
import uuid

logger = logging.getLogger("psi8400")

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
        transportid = 0
        json_encode = json.loads(jsonpickle.encode(self, unpicklable = False))

        for jsdau in json_encode["psi8400DauConfigList"]:
            jsdau["psi8400Config"] = None
            for js_multisensor_config in jsdau["multiSensorConfigList"]:
                js_multisensor_config["psi8400Config"] = None
                js_multisensor_config["multiSensor"]["psi8400Config"] = None
                js_multisensor_config["dauConfig"]["psi8400Config"] = None
                psi8400MultiSensorConfig_id = transportid 
                transportid = transportid + 1
                js_multisensor_config["@transportid"] = psi8400MultiSensorConfig_id 
                for js_psi_channel in js_multisensor_config["channelConfigList"]:
                    js_psi_channel["psi8400MultiSensorConfig"] = psi8400MultiSensorConfig_id

                if js_multisensor_config["pcuConfig"] != None:
                    js_multisensor_config["pcuConfig"]["psi8400Config"] = None

        for jspcu in json_encode["psi8400PCUConfigList"]:
            jspcu["psi8400Config"] = None

        return json.dumps(json_encode, sort_keys = True, indent = 4)

    @classmethod
    def decode_json(cls, json_encode):
        if "@transportid" in json_encode: del json_encode["@transportid"]

        json_encode["py/object"] = "__main__.psi8400"

        if "psi8400DauConfigList" in json_encode:
            for jsdau in json_encode["psi8400DauConfigList"]:
                jsdau["py/object"] = "__main__.psi8400_dau_config"
                if "@transportid" in jsdau: del jsdau["@transportid"]
                for js_multisensor_config in jsdau["multiSensorConfigList"]:
                    js_multisensor_config["py/object"] = "__main__.psi8400_multi_sensor_config"
                    js_multisensor_config["multiSensor"]["py/object"] = "__main__.multisensor"
                    for js_psi_channel in js_multisensor_config["channelConfigList"]:
                        js_psi_channel["py/object"] = "__main__.psi8400_channel_config"

        if "psi8400PCUConfigList" in json_encode:
            for jspcu in json_encode["psi8400PCUConfigList"]:
                jspcu["py/object"] = "__main__.psi8400_pcu_config"

                if "@transportid" in jspcu: del jspcu["@transportid"]

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
    logger.debug("psi reponse %s" % psi_obj.to_JSON())

def read_psi(windtest_id):
    session = login()
    r = session.get(satis_url + "windtest/%s/reference/master/psi8400config/getlist/" % windtest_id)
    logger.debug("repondre %s" % r.json())
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

def main():
    from datetime import datetime
    logger.info("Start configure satis")
    
    windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    wt = create_windtest(windtest_id)
    windtest_id = wt.id
    #remove_all_psi(windtest_id)
    create_psi(windtest_id, logicalName = "PSI8400", physicalName = "F1-PSI249")
    psi_obj = read_psi(windtest_id)
    logger.debug("psi encode json %s" % psi_obj.to_JSON())
    logger.debug("obj loop %s" % psi_obj.psi8400DauConfigList[0])
    logger.debug("obj loop %s" % psi_obj.psi8400DauConfigList[0].multiSensorConfigList[0].multiSensor.id)
    logger.debug("obj loop %s" % psi_obj.psi8400DauConfigList[0].multiSensorConfigList[0].multiSensor.id)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
