from socket import *
import select
import json
import time
import requests
from requests import Request

from maxsmart_http import MaxsmartHttp

class Device:
    def __init__(self, data, ip):
        self.name = data['name']
        self.sn = data['sn']
        self.sak = data['sak']
        self.ip = ip

class Explorer:
    def discover(self, broadcast_address):
        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
        cs.sendto('00dv=all,2017-10-28,14:09:00,34;', (broadcast_address, 8888))
        cs.setblocking(0)

        timeToWaitInSeconds = 2
        start_time = time.time()
        devices = []

        while time.time() - start_time <= timeToWaitInSeconds:
            ready = select.select([cs], [], [], timeToWaitInSeconds)

            if ready[0]:
                # A buffer of 1024 is also used in the Android app of MaxSmart.
                # We assume this suffices.
                data, address = cs.recvfrom(1024)
                parsed = json.loads(data)
                devices.append(Device(parsed['data'], address[0]))

        return devices

    def status(self, device):
        response = MaxsmartHttp.send(device, 511)

        return response.json()['data']

    def switch(self, device, status):
        new_state = 1 if status == 'on' else 0
        options = {'sn': device.sn, 'port': '0', 'state': new_state}

        MaxsmartHttp.send(device, 200, options)

    def set_name(self, device, name):
        options = {'sn': device.sn, 'port': '0', 'name': name}

        MaxsmartHttp.send(device, 201, options)
