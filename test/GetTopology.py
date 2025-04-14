from opensearchpy import OpenSearch
from Olt import Olt
from Onu import Onu
import json

OPENSEARCH_HOST = '132.177.253.4'
OPENSEARCH_PORT = 9200
OPENSEARCH_USER = 'admin'
OPENSEARCH_PASSWORD = 'Obcas@2024'
OPENSEARCH_CA_CERT_PATH = './root-ca.pem'


class Topology:
    def __init__(self):
        self.olts = None
        self.onus = None
        self.client = OpenSearch(
            hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
            http_compress=True,
            http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
            use_ssl=True,
            verify_certs=True,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
            ca_certs=OPENSEARCH_CA_CERT_PATH
        )

    def load_topology(self):
        print("Loading Topology")

        onus_response = self.client.search(
            index="obcas-onu-topology",
            body={
                "query": {
                    "match_all": {}
                }
            },
            size=100
        )

        olt_onus = {}
        self.onus = []

        for onu_source in onus_response["hits"]["hits"]:
            onu = onu_source["_source"]

            onu_obj = Onu(onu)

            olt = onu["olt"]
            if olt in olt_onus.keys():
                olt_onus[olt].append(onu_obj)
            else:
                olt_onus[olt] = [onu_obj]

            self.onus.append(onu_obj)

        olts_reponse = self.client.search(
            index="obcas-olt-topology",
            body={
                "query": {
                    "match_all": {}
                }
            }
        )

        with open('topology.json', 'r') as file:
            endpoints = json.load(file)

        self.olts = []
        for olt in olts_reponse["hits"]["hits"]:
            if olt["_source"]["deviceRefId"] not in endpoints.keys():
                print(f"{olt['_source']['deviceRefId']} not in topology")
                exit(0)
            else:
                host = endpoints[olt["_source"]["deviceRefId"]]["host"]
                port = endpoints[olt["_source"]["deviceRefId"]]["port"]
                resources = endpoints[olt["_source"]["deviceRefId"]]["resources"]
                connected_onus = olt_onus[olt["_source"]["deviceRefId"]]

                olt_obj = Olt(olt["_source"], host, port, resources, connected_onus)

                for connected_onu in connected_onus:
                    connected_onu.set_olt_ref(olt_obj)

                self.olts.append(olt_obj)
