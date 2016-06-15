from satis_webapp import login, satis_url
import json
import logging

logger = logging.getLogger("windtest")

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

def main():
    from datetime import datetime
    windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    wt = create_windtest(windtest_id)
    windtest_id = wt.id


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
