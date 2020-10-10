from subprocess import check_output
#import re
import objc
import sys
import requests

def scan_networks():
    airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -s"
    rc = check_output(airport, shell=True).decode("utf-8").split("\n")[1:-1]
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
    print("Current network name:")

def update_stock_firmware():
    print("Updating Stock Firmware..")

def update_to_new_firmware():
    print("Update to New Firmware..")

if sys.platform=="darwin":
    current_network_name = get_current_network_name()
    network_names = scan_networks()
    for network in network_names:
        if "shelly" in network:
            connect_to_wifi_network(network,None)
            pload = {'ssid': '<your_home_network_ssid', 'key': '<your_home_network_password'}
            r = requests.post('http://localhost/settings/sta',data=pload)
            connect_to_wifi_network('<your_home_network_ssid','<your_home_network_password')
            update_stock_firmware()
            update_to_new_firmware()





