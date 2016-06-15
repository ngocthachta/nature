from windtest import create_windtest
#from safin import read_safin, create_safin_stationnaire, create_safin_instationnaire
from safin import *
from psi8400 import *
from scale import *
import logging
import json

logger = logging.getLogger("satis_util")


def main():
    from datetime import datetime
    logger.info("Start configure satis")
    
    windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    wt = create_windtest(windtest_id)
    windtest_id = wt.id

    safin_obj = create_safin_stationnaire(windtest_id, logicalName = "SafinStationnaire", physicalName = "F1-SAFIN225",
             nb_module_safin = 16)
    create_safin_instationnaire(windtest_id, logicalName = "SafinDynamique", nb_module_safin = 4)
    create_psi(windtest_id, logicalName = "PSI8400", physicalName = "F1-PSI249")
    create_scale(windtest_id, logicalName = "Balance_0", physicalName = "PHI190-02", safin_obj = safin_obj)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
