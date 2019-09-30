import requests
import json
import pprint
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os,sys

def get_best_stop_id(name):
    print(name)
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url='https://keyvaulttest-2.vault.azure.net/', credential=credential)
    secret_transport_nsw = secret_client.get_secret("transport-nsw")
    headers={'Authorization': secret_transport_nsw.value}

    stop_payload = {
        'outputFormat' : 'rapidJSON',
        'type_sf' : 'any',
        'coordOutputFormat' : 'EPSG:4326',
        'name_sf' : name,
        'version' : '10.2.1.42'
    }
    headers={'Authorization': secret_transport_nsw.value}
    stop_response = requests.get('https://api.transport.nsw.gov.au/v1/tp/stop_finder',params=stop_payload,headers=headers)
    stop_response = stop_response.json()

    #print(stop_response['locations'])

    for stop in stop_response['locations']:
        if stop['isBest'] == True:
            #print(stop['isBest'])
            #print(stop['id'])
            return(stop['id'])
        else:
            pass


if __name__ == '__main__':
    print(get_best_stop_id('Parramatta Station'))
