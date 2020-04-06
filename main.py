from time import sleep, ctime, time
from requests import get
from requests.exceptions import ConnectionError, ReadTimeout
from os import getenv
from sys import exit
from signal import signal, SIGINT, SIGTERM
from urllib3.exceptions import MaxRetryError, ReadTimeoutError

def log_msg(msg, level='INFO'):
    print("[%s] - %s : %s" % (level, ctime(time()), msg))

def handler_stop_signals(signum, frame):
    log_msg("Stoping", "INFO")
    exit(0)

signal(SIGINT, handler_stop_signals)
signal(SIGTERM, handler_stop_signals)

try:
    token=open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r').read()
    namespace=open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r').read()
except (IOError) as e:
    log_msg('{}'.format(e), "ERROR")
    exit(1)

service_host = getenv('KUBERNETES_SERVICE_HOST', '127.0.0.1')
sevice_port = getenv('KUBERNETES_PORT_443_TCP_PORT', '443')
sleeping = getenv('SLEEP', '1')
timeout =  getenv('TIMEOUT', '1')

log_msg("Starting", "INFO")

while True:
    try:
       pods = get('https://' + service_host + ':' + sevice_port + '/api/v1/namespaces/' + namespace + '/pods/', verify='/var/run/secrets/kubernetes.io/serviceaccount/ca.crt', headers={'Authorization': 'Bearer ' + token}, timeout=int(timeout))

       if pods.status_code == 200:
           log_msg('[{}] Listed {} pods'.format(pods.elapsed.total_seconds(), len(pods.json()['items'])))
       else:
           log_msg('[{}] {} - {}'.format(pods.elapsed.total_seconds(), pods.status_code, pods.text), 'ERROR')

    except (MaxRetryError, ConnectionError, ValueError, ReadTimeout, ReadTimeoutError) as e:
        log_msg('{}'.format(e), "ERROR")

    sleep(int(sleeping))
