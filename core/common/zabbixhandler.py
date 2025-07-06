import os

import requests
from dotenv import load_dotenv

load_dotenv()

class ZabbixHandler:
    def __init__(self):
        self.zabbix_url = os.getenv("ZABBIX_URL")
        self.zabbix_username = os.getenv("ZABBIX_USER")
        self.zabbix_password = os.getenv("ZABBIX_PASSWORD")
        self.zabbix_auth_token = None

    def login(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "username": self.zabbix_username,
                "password": self.zabbix_password
            },
            "id": 1
        }
        response = requests.post(self.zabbix_url, json=payload)
        response.raise_for_status()
        return response.json()["result"]

    # Buscar triggers ativas com filtro por descrição
    def get_active_triggers_by_description(self, auth_token, hostid=None, partial_description=None):
        payload = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": [
                    "description",
                    "value"
                ],
                "only_true": True,
                "search": {
                    "description": partial_description,
                },
                "searchByAny": True,
                "searchWildcardsEnabled": True,
                "expandDescription": True,
                "selectHosts": ["hostid", "host"]
            },
            "auth": auth_token,
            "id": 2
        }

        if hostid:
            payload["params"]["hostids"] = hostid

        response = requests.post(self.zabbix_url, json=payload)
        response.raise_for_status()
        return response.json()["result"]

    def get_only_true_triggers(self, auth_token):
        payload = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "only_true": True,  # apenas triggers em estado de problema
                "expandDescription": False,
                "selectHosts": ["hostid", "host"]
            },
            "auth": auth_token,
            "id": 2
        }

        response = requests.post(self.zabbix_url, json=payload)
        response.raise_for_status()
        return response.json()["result"]

    def get_triggers_by_host(self, auth_token, host=None):
        payload = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "expandDescription": False,
                "only_true": True,
                "host": host,
                "selectHosts": ["hostid", "host"]
            },
            "auth": auth_token,
            "id": 2
        }
        print(payload)

        response = requests.post(self.zabbix_url, json=payload)
        response.raise_for_status()
        return response.json()["result"]

