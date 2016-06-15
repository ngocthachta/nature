from windtest import windtest_object

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

