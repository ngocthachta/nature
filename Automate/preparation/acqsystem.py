from windtest import windtest_object

import jsonpickle
import json

class acqsystem(windtest_object):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "WindTestObject",
            logicalName = "", physicalName = "", isValid = False, acqSystemType = "", address = ""):
        windtest_object.__init__(self, windTestId = windTestId, reference = reference, id = id,
                type = type)
        self.logicalName = logicalName
        self.physicalName = physicalName
        self.isValid = isValid
        self.acqSystemType = acqSystemType
        self.address = address

class device_config_handled_by_a_clock(acqsystem):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "WindTestObject",
            logicalName = "", physicalName = "", isValid = False, acqSystemType = "", 
            address = "",
            defaultClock = "HDEV", defaultFrequenceRest = 1.0, frameSize = 1000, 
            acquisitionMode = "CONTINUE",
            hsyncDeviceAddress = "",
            usedSynchronizingClock = False):
        acqsystem.__init__(self, windTestId = windTestId, reference = reference, id = id, 
                type = type, logicalName = logicalName, physicalName = physicalName, isValid = isValid, 
                acqSystemType = acqSystemType, address = address)
        self.defaultClock = defaultClock
        self.defaultFrequenceRest = defaultFrequenceRest
        self.frameSize = frameSize
        self.acquisitionMode = acquisitionMode
        self.hsyncDeviceAddress = hsyncDeviceAddress
        self.usedSynchronizingClock = usedSynchronizingClock

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

class configuration_element(windtest_object):
    def __init__(self, windTestId = "", reference = "master", id = None, type = "ConfigurationElement",
            deviceConfigId = None, name = "", data = None, content_type = "", 
            content_enricher = "", content_link = [], understandableByTheDevice = False):
        windtest_object.__init__(self, windTestId = windTestId, reference = reference, id = id,
                type = type)
        self.deviceConfigId = deviceConfigId
        self.name = name
        self.data = data
        self.content_type = content_type
        self.content_enricher = content_enricher
        self.content_link = content_link
        self.understandableByTheDevice = understandableByTheDevice

    def to_JSON(self):
        json_encode = json.loads(jsonpickle.encode(self, unpicklable = False))
        return json.dumps(json_encode, sort_keys = True, indent = 4)

    @classmethod
    def decode_json(cls, json_encode):
        if "@transportid" in json_encode: del json_encode["@transportid"]
        json_encode["py/object"] = "__main__.configuration_element"

        return jsonpickle.decode(json.dumps(json_encode))

