from urllib import request, error
from time import sleep
import logging
from configparser import ConfigParser

configfile_name = "duckupdate.conf"
config = ConfigParser()
config.read_file(open(configfile_name))

DOMAIN = config['DEFAULT']['DOMAIN']
TOKEN = config['DEFAULT']['TOKEN']
SLEEPTIME = config['DEFAULT']['SLEEPTIME']

UPDATEURL = 'https://www.duckdns.org/update?domains={domain}&token={token}&ip={external_ip}&verbose=true&clear=true'

def httprequest(url):
    try:
        return request.urlopen(url).read().decode('utf8')
    except error.URLError as e:
        logging.error('URL Errror :', e.reason)
    except error.HTTPError as e:
        logging.error('HTTP Error code :', e.code)
        logging.error('HTTP Errot reason :', e.reason)
    except Exception:
        import traceback
        logging.error('generic exception: ' + traceback.format_exc())

def getExternalIP():
    return httprequest('https://ident.me')

def updateDuckDNS(external_ip, domain, token):
    result = httprequest(UPDATEURL.format(external_ip=external_ip, 
                                          domain=domain,
                                          token=token))
    return result.split()[0], result.split()[-1] 
        
def update():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s : %(message)s', level=logging.DEBUG)
    logging.info('Query External IP ...')
    external_ip = getExternalIP()
    if external_ip:
        logging.info('external ip : {} '.format(external_ip)) 
        res, status = updateDuckDNS(external_ip, DOMAIN, TOKEN)
        if res == 'OK':
            logging.info('external ip : {extip} status : {stat}'.format(extip=external_ip, stat=status))
        else:
            logging.error('Bad Response ')

if __name__ == "__main__":
    try:
        while True:
            update()
            sleep(int(SLEEPTIME))
    except KeyboardInterrupt:
        logging.info('Interupt By Ctrl-C')