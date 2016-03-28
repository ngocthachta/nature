import logging
import numpy
logger = logging.getLogger("Optimize Finance")

APPORT = 102000
PTZ = 75600
PROJET_1 = 276895
PROJET_2 = 265702

def calcul_pas_schedule_1(pas_fix = 99295.0, taux = 2.2, during = 25.0):
    result = 0
    taux = taux / 100.0
    # result = p * X / Y
    index = numpy.array([0.0] * (during + 1))
    index[0] = 1
    index[1] = 1
    for i in range(2, during +1):
        new_index = numpy.array([0.0] * (during + 1))
        new_index[0] = 1
        new_index[i] = 1
        middle = int(during / 2 if during % 2 == 0 else during/2 + 1)
        for j in range(1, middle + 1):
            new_index[j] = index[j - 1] + index[j]
            new_index[i-j] = index[i-j] + index[i - j - 1]

        index = new_index.copy()
    X = 0
    for i, coef in enumerate(index):
        X = X + coef * pow(taux, i)
    Y = 0
    for i, coef in enumerate(index[1:]):
        Y = Y + coef * pow(taux, i)

    result = round(pas_fix * (X / Y) / 12.0, 2)

    #logger.debug("index of %s : %s" % (during, index))
    return result

def optimize(projet = PROJET_1, during = 25, taux = 2.2, unblocking_period = 3, 
        unblocking_taux = 2.7, ptz_insurance = 31.02, pas_insurance = 40.75):
    pas_fix = (projet - APPORT - PTZ)
    pas_schedule_0 = round(pas_fix * unblocking_taux / 100.0 / 12.0, 2)

    logger.debug("pas_schedule_0 calcul =%s" % pas_schedule_0)

    ptz_pallier_0, ptz_pallier_1, ptz_pallier_2 = unblocking_period, 10, 12
    ptz_schedule_0, ptz_schedule_1, ptz_schedule_2 = 0, 0, 525 * 12
    ptz = ptz_pallier_0 * ptz_schedule_0 + ptz_pallier_1 * ptz_schedule_1 + \
            ptz_pallier_2 * ptz_schedule_2 
    ptz_insurance_total = (ptz_pallier_0 + ptz_pallier_1 + ptz_pallier_2) * ptz_insurance * 12
    
    
    pas_pallier_0, pas_pallier_1 = unblocking_period, during

    remain_to_repay = pas_fix

    frais = 0
    my_pais = 0
    
    for i in range(unblocking_period):
        frais_annuel = remain_to_repay * unblocking_taux / 100.0
        pas_return = (pas_schedule_0) * 12.0 
        remain_to_repay = remain_to_repay - pas_return + frais_annuel 
        frais = frais + frais_annuel
        my_pais = my_pais + pas_return
    
    logger.debug("remain_to_repay after unblocking period = %s" % remain_to_repay)
    frais = 0
    new_tax = (taux * (during + unblocking_period)  - unblocking_taux * unblocking_period) \
                / during
    logger.info("new taux for pallier 1 = %s" % new_tax)
    pas_schedule_1 = calcul_pas_schedule_1(pas_fix = remain_to_repay, taux = new_tax, during = during)
    logger.debug("pas_schedule_1 calcul =%s" % pas_schedule_1)

    for i in range(during):
        frais_annuel = remain_to_repay * new_tax / 100.0 # why 2.135 in place of 2.20
        pas_return = (pas_schedule_1) * 12.0 
        remain_to_repay = remain_to_repay - pas_return + frais_annuel 
        frais = frais + frais_annuel
        my_pais = my_pais + pas_return

    pas_insurance_total = (pas_pallier_0 + pas_pallier_1) * pas_insurance * 12.0 

    logger.debug("frais in unblocking period = %s" % frais)
    logger.debug("frais = %s" % frais)
    logger.debug("my pais =  %s" % my_pais)
    logger.debug("remain_to_repay = %s" % remain_to_repay)
    logger.info("projet = %s" % projet)
    logger.info("apport = %s" % APPORT)
    logger.info("ptz = %s" % ptz)
    logger.info("pas fix = %s" % pas_fix)
    logger.info("ptz insurance = %s" % ptz_insurance_total)
    logger.info("pas inssurance = %s" % pas_insurance_total)
    logger.info("inssurance total = %s" % (pas_insurance_total + ptz_insurance_total))

def main():
    logger.info("Start programme for projet 1")
    logger.info("*" * 30)
    optimize(projet = PROJET_1, ptz_insurance = 31.02, pas_insurance = 40.75)
    logger.info("*" * 30)

    logger.info("Start programme for projet 2")
    logger.info("*" * 30)
    optimize(projet = PROJET_2, ptz_insurance = 31.02, pas_insurance = 36.17)
    logger.info("*" * 30)
    #calcul_pas_schedule_1(during = 5)


if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG, 
            format = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            datefmt = '%Y-%m-%d %H:%M:%S')
    main()
