#!/usr/bin/env python3

"""{"ip":"","port":27008,"tport":27018,"cport":9605,"name":"AC DRIFT3RS Public Drift Server! | ADC Pack 420 | LA Canyons","clients":3,"maxclients":20,"track":"la_canyons-freeroam","cars":["adc_bmw_e36_m3__420","adc_bmw_e92_m3_low__420","adc_lexus_is200__420","adc_lexus_is200_xe-10__420","adc_mazda_fc__420","adc_mazda_rx7__420","adc_nissan_180sx__420","adc_nissan_350z__420","adc_nissan_fairlady_432__420","adc_nissan_s13__420","adc_nissan_s14_dsa__420","adc_nissan_s14_zenki__420","adc_nissan_s15__420","adc_nissan_silvia_s13_luke_v","adc_nissan_skyline_r31__420","adc_nissan_skyline_r32__420","adc_toyota_cresta__420","adc_toyota_jzx100_chaser__420","adc_toyota_soarer__420"],"timeofday":-48,"session":0,"sessiontypes":[1],"durations":[360],"timeleft":5877,"country":["na","na"],"pass":false,"timestamp":0,"json":null,"l":false,"pickup":true,"timed":true,"extra":false,"pit":false,"inverted":0}
"""

import urllib.request
import json
import jmespath
import os

def get_json(url):
        url = urllib.request.urlopen(f"{server_address}:{port}/INFO")
        return json.loads(url.read().decode())

class Server:
    def __init__(self, json):
        self.json = json
        self.name = jmespath.search('name', json)
        self.maxclients = jmespath.search('maxclients', json)
        self.clients = jmespath.search('clients', json)
        self.track = jmespath.search('track', json)
        self.metricsfile = './file'

    def delete_file(data):
        try:
            os.remove(self.metricsfile)
        except:
            print('dupa')
    

    def write_to_file(data):
        with open(self.metricsfile, 'w') as f:
            f.write(data)
            f.close()

    def return_data(self):
        data = {'name': self.name,
                'clients': self.clients,
                'maxclients': self.maxclients,
                'track': self.track}
        return data

    def return_metrics(self):
        data = f"# HELP server players online\n"\
                f"# TYPE server_name summary\n"\
                "server_online_players{" + f"server_name='{self.name}'" + "} " + f"{self.clients}"
        return data

    def return_metrics_to_file(self):
        f = open(self.metricsfile, 'w')
        f.write('# HELP server players online')
        f.write('# TYPE server_name summary')
        s = "server_online_players{" + 'server_name="' + f"{self.name}" + '"}' + f" {self.clients}"
        f.write(s)
        #f.write('"server_online_players{" + f"server_name=\'{self.name}\'" + "} " + f"{self.clients}"')
        f.close()


if __name__ == "__main__":
    server_address = 'http://sunny-motorsports.com'
    ports_to_scan = [9601, 9602, 9603, 9604, 9605, 9606, 9607]

    servers = []

    for port in ports_to_scan:
        server = Server(get_json(f"{server_address}:{port}/INFO"))
        servers.append(server)
        #servers.append(get_json(f"{server_address}:{port}/INFO"))
        #print(json.dumps(data, indent=4, sort_keys=True))

    servers[0].delete_file()
    data = []

    for server in servers:
        print(server.return_metrics())
        for line in server.return_metrics():
            data.append(line)

    file = "./file"

    f = open(file, 'w')
    for line in data:
            f.write(line)

    f.close()
        #server.return_metrics_to_file()
        #print(json.dumps(server, indent=4, sort_keys=True))