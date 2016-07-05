from windtest import create_windtest
#from safin import read_safin, create_safin_stationnaire, create_safin_instationnaire
from safin import *
from psi8400 import *
from genericdevice import *
from scale import *
from usermodule import *
import logging
import json

logger = logging.getLogger("satis_util")


def main():
    from datetime import datetime
    logger.info("Start configure satis")
    
    #windtest_id = "Windtest%s" % datetime.now().strftime("%Y%m%d%H%M%S")
    windtest_id = "Test_MORPHO_F1Plus_2016_R8"
    wt = create_windtest(windtest_id)
    windtest_id = wt.id

    safin_obj = create_safin_stationnaire(windtest_id, logicalName = "SafinStationnaire", physicalName = "F1-SAFIN225",
             nb_module_safin = 8)
    safindyn_obj = create_safin_instationnaire(windtest_id, logicalName = "SafinDynamique", nb_module_safin = 6)
    create_psi(windtest_id, logicalName = "PSI8400", physicalName = "F1-PSI249")
    create_barometre(windtest_id, logicalName = "Barometre", \
            physicalName = "F1-BARO50")
    create_scale(windtest_id, logicalName = "BalanceMonomat", physicalName = "PHI190-02", safin_obj = safin_obj)
    create_scale(windtest_id, logicalName = "BalanceDynamique", physicalName = "PHI190-02", safin_obj = safindyn_obj)
    create_user_module(windtest_id, logicalName = "iumod_1", usmtype = "InterpreterUserModule")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
