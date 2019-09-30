from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url='https://keyvaulttest-2.vault.azure.net/', credential=credential)
secret_mapbox = secret_client.get_secret("mapbox")
secret_transport_nsw = secret_client.get_secret("transport-nsw")

MAPBOX_ACCESS_KEY = secret_mapbox.value
TRANSPORT_NSW_ACCESS_KEY = secret_transport_nsw.value