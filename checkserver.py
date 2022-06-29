#!/usr/bin/env python3

import urllib.request
import json
import jmespath
import os
import time

FILE='metrics_ac'

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


    def return_data(self):
        data = {'name': self.name,
                'clients': self.clients,
                'maxclients': self.maxclients,
                'track': self.track}
        return data

    def return_metrics(self, instance_number):
        data = [f"# HELP server players online\n",
                f"# TYPE server_name summary\n",
                f"server_online_players_server_{instance_number}" + "{" + f'server_name="{self.name}"' + "} " + f"{self.clients}\n"]
        return data


if __name__ == "__main__":
    server_address = 'hostname'
    ports_to_scan = [9601, 9602, 9603, 9604, 9605, 9606, 9607]

    servers = []

    for port in ports_to_scan:
        server = Server(get_json(f"{server_address}:{port}/INFO"))
        servers.append(server)

    data = []

    try:
        os.remove(FILE)
    except:
        print("no file")
    f = open(FILE, 'w')

    for server in servers:
        instance_number = servers.index(server) + 1
        for line in server.return_metrics(instance_number):
            print(line)
            f.write(line)
            #time.sleep(5)

    f.close()
