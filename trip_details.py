import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os,sys
import requests
import json
import pprint
from datetime import date, datetime
from get_best_stop_id import get_best_stop_id
from numpy import linspace
from get_sunposition import sun_position
from geometry_transformations import points_from_bearing
from math import radians

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url='https://keyvaulttest-2.vault.azure.net/', credential=credential)
secret_transport_nsw = secret_client.get_secret("transport-nsw")
headers={'Authorization': secret_transport_nsw.value}

def get_trips_details(origin_name,destination_name,time):
    origin_id = get_best_stop_id(origin_name)
    destination_id = get_best_stop_id(destination_name)

    tt = time[:10].replace("-","")
    tt2 = time[11:16].replace(":","")
    
    payload = {
     'outputFormat' : 'rapidJSON',
     'coordOutputFormat' : 'EPSG:4326',
     'depArrMacro' : 'dep',
     'itdDate' : tt,
     'itdTime' : tt2,
     'type_origin' : 'stop',
     'name_origin' : origin_id, 
     'type_destination' : 'stop',
     'name_destination' : destination_id, 
     'TfNSWTR' : 'true',
     'calcNumberOfTrips' : 1,
     'excludedMeans' : 'checkbox',
     'exclMOT_4': 1,
     'exclMOT_5': 1,
     'exclMOT_7': 1,
     'exclMOT_9': 1,
     'exclMOT_11': 1
     }

    response = requests.get('https://api.transport.nsw.gov.au/v1/tp/trip',params=payload,headers=headers)
    json_response = response.json()
    departure_time = json_response['journeys'][0]['legs'][0]['origin']['departureTimePlanned']
    arrival_time = json_response['journeys'][0]['legs'][0]['destination']['arrivalTimePlanned']

    p = '%Y-%m-%dT%H:%M:%SZ'
    epoch = datetime(1970, 1, 1)
    departure_time_epoch = int((datetime.strptime(departure_time, p) - epoch).total_seconds())
    arrival_time_epoch = int((datetime.strptime(arrival_time, p) - epoch).total_seconds())

    journey_coords = json_response['journeys'][0]['legs'][0]['coords']
    journey_lat = [x[0] for x in journey_coords]
    journey_lon = [x[1] for x in journey_coords]

    time_schedule = linspace(departure_time_epoch, arrival_time_epoch, len(journey_lat))
    time_schedule = [int(x) for x in time_schedule]
    
    trip_df = pd.DataFrame({'lat' : journey_lat, 'lon' : journey_lon, 'heading' : 0 , 'lead_lat': journey_lat[1:]+[0] , 'lead_lon': journey_lon[1:]+[0], 'epoch_time': time_schedule })
    trip_df['timeit'] = pd.to_datetime(trip_df['epoch_time'],unit='s')
    trip_df['date'] = pd.to_datetime(trip_df["timeit"].dt.strftime('%Y-%m-%dT%H:%M:%SZ'))
    trip_df['date2'] = trip_df.timeit.map(lambda x: datetime.strftime(x, '%Y-%m-%dT%H:%M:%SZ'))
    trip_df['midpoint_lat'] = (trip_df['lat'].iloc[0]+trip_df['lat'].iloc[-1])/2
    trip_df['midpoint_lon'] = (trip_df['lon'].iloc[0]+trip_df['lon'].iloc[-1])/2
    trip_df['sun_position'] = 0
    trip_df['sun_position2'] = sun_position(trip_df['midpoint_lat'], trip_df['midpoint_lon'], trip_df['timeit']) #keep the first lat and lon constant 
    trip_df['sun_pos_lon'] = trip_df.apply(lambda x: points_from_bearing(x['midpoint_lat'], x['midpoint_lon'], x['sun_position2'],10,'lon'),axis=1)
    trip_df['sun_pos_lat'] = trip_df.apply(lambda x: points_from_bearing(x['midpoint_lat'], x['midpoint_lon'], x['sun_position2'],10,'lat'),axis=1)
    print("Trip Details Complete")
    return trip_df

if __name__ == "__main__":
    get_trips_details('Parramatta Station','Central Station','2019-10-25T22:30:03')