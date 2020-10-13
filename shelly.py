import subprocess
import logging
import sys
import functools
import getpass
#import re

logging.TRACE = 5
logging.addLevelName(logging.TRACE, 'TRACE')
logging.Logger.trace = functools.partialmethod(logging.Logger.log, logging.TRACE)
logging.trace = functools.partial(logging.log, logging.TRACE)
logging.basicConfig(format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
  import objc
except ImportError:
  logger.info("Installing PyobjC...")
  pipe = subprocess.check_output(['pip3', 'install','-U','pyobjc'])
  import objc
try:
  import requests
except ImportError:
  logger.info("Installing requests...")
  pipe = subprocess.check_output(['pip3', 'install', 'requests'])
  import requests

def scan_networks():
    airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -s"
    rc = subprocess.check_output(airport, shell=True).decode("utf-8").split("\n")[1:-1]
    networks =[]
    for i in rc:
        i = i.lstrip().rstrip()
        # mac = re.search(r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", i, re.I).group()
        # rssi = re.search(r"\-(\d)\w+", i, re.I).group()
        networks.append(i.split(" ")[0])
    return networks


def connect_to_wifi_network(network_name,network_pass):
    objc.loadBundle('CoreWLAN',bundle_path = '/System/Library/Frameworks/CoreWLAN.framework',module_globals = globals())
    iface = CWInterface.interface()
    networks, error = iface.scanForNetworksWithName_error_(network_name, None)
    network = networks.anyObject()
    success, error = iface.associateToNetwork_password_error_(network,network_pass, None)

def get_current_network_name():
    airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
    rc = subprocess.check_output(airport, shell=True).decode("utf-8").split("\n")
    for i in rc:
        i = i.lstrip().rstrip()
        if ('BSSID' not in i) & ('SSID:' in i) :
            return i.replace('SSID:','').lstrip().rstrip()


def connect_to_home_wifi():
    if sys.platform=="darwin":
        print("searching for shelly devices on AP mode..")
        current_network_name = get_current_network_name()
        network_names = scan_networks()
        combined = '\t'.join(network_names)
        if "o" not in combined:
            print("No shelly devices found / all shelly devices already connected to home wifi")
        else:
            try:
                p = getpass.getpass(prompt='Please enter Home wifi Password: ', stream=None)
            except Exception as error:
                print('ERROR', error)
            else:
                for network in network_names:
                    if "o" in network:
                        try:
                            connect_to_wifi_network(network,None)
                            pload = {'ssid': current_network_name, 'key': p}
                            r = requests.post('http://localhost/settings/sta',data=pload)
                        except Exception as error:
                            print('ERROR', error)
                connect_to_wifi_network(current_network_name,p)


connect_to_home_wifi()

