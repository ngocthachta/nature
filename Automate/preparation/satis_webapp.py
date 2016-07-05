import requests
import os
import logging

logger = logging.getLogger("satis_webapp")

satis_url = "http://localhost:8081/satis/"
#satis_url = "http://192.168.85.230:8081/satis/" #demo1

def create_session(user="user", password="password"):
    os.environ['NO_PROXY'] = 'localhost'
    session = requests.Session()
    session.auth = (user, password)
    return session

def login(url="http://localhost:8081/satis/login", user="user", password="password"):
    session = create_session()
    r = session.get(url, auth=(user, password))
    return session

def main():
    r = login()
    logger.info("repondre : %s" % r)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
