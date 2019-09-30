from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, render_template, flash
from datetime import date, datetime
import get_best_stop_id
import get_sunposition
from trip_details import get_trips_details
import pandas as pd
import json
import time

app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('APP_CONFIG_FILE')
MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']
TRANSPORT_NSW_ACCESS_KEY = app.config['TRANSPORT_NSW_ACCESS_KEY']
app.secret_key = 'wicked'

execution_counter = 0
user_origin = 'Parramatta Station'
user_destination = 'Central Station'
user_time = '2019-10-10T10:30:03'
trip_details = get_trips_details(user_origin,user_destination,user_time)
coords_list = [[trip_details['lon'][val],trip_details['lat'][val]] for val in range(0,len(trip_details))]
#sun_list = trip_details['sun_pos']
#[[trip_details['sun_pos'][val],trip_details['sun_pos'][val]] for val in range(0,len(trip_details))]
sun_list = [[trip_details['sun_pos_lon'][val],trip_details['sun_pos_lat'][val]] for val in range(0,len(trip_details))]
#print(coords_list)



@app.route('/mapbox_gl', methods=['POST','GET'])
def mapbox_gl():
    print("I am called")
    a = get_user_trip_details()
    global user_origin, user_destination, user_time
    global execution_counter
    global trip_details, coords_list, sun_list
    
    print("this has fired", execution_counter, "times")
    print("User_Time", user_time)
    
    getters()
    user_time = session.get('my_var', None)

    print('getters returned',user_time)


    if a is not None and execution_counter > 0:
        print("POST Returned")
        print(a)
        if a['id'] == 'destination':
            user_destination = a['data']
            try:
                #print(user_origin, user_destination)
                trip_details = get_trips_details(user_origin, user_destination,user_time)
                coords_list = [[trip_details['lon'][val],trip_details['lat'][val]] for val in range(0,len(trip_details))]
                sun_list = [[trip_details['sun_pos_lon'][val],trip_details['sun_pos_lat'][val]] for val in range(0,len(trip_details))]

            except NameError:
                print('here 2')
                print('origin not user defined, so set it to default')
                trip_details = get_trips_details('Parramatta Station', user_destination,user_time)
                coords_list = [[trip_details['lon'][val],trip_details['lat'][val]] for val in range(0,len(trip_details))]
                sun_list = [[trip_details['sun_pos_lon'][val],trip_details['sun_pos_lat'][val]] for val in range(0,len(trip_details))]
        else:
            user_origin = a['data']
            #print(user_origin)
            try:
                trip_details = get_trips_details(user_origin, user_destination,user_time)
                coords_list = [[trip_details['lon'][val],trip_details['lat'][val]] for val in range(0,len(trip_details))]
                sun_list = [[trip_details['sun_pos_lon'][val],trip_details['sun_pos_lat'][val]] for val in range(0,len(trip_details))]

            except NameError:
                print('destination not user defined, so set it to default')
                trip_details = get_trips_details(user_origin, 'Central Station',user_time)
                coords_list = [[trip_details['lon'][val],trip_details['lat'][val]] for val in range(0,len(trip_details))]
                sun_list = [[trip_details['sun_pos_lon'][val],trip_details['sun_pos_lat'][val]] for val in range(0,len(trip_details))]
    
        print("i've finished")

    elif execution_counter > 0:
        print("time has changed")
        trip_details = get_trips_details(user_origin, user_destination,user_time)
        coords_list = [[trip_details['lon'][val],trip_details['lat'][val]] for val in range(0,len(trip_details))]
        sun_list = [[trip_details['sun_pos_lon'][val],trip_details['sun_pos_lat'][val]] for val in range(0,len(trip_details))]
        session['reload_val'] = 2
        load_refresh()

    execution_counter = execution_counter + 1
    
    return render_template(
        'mapbox_gl.html', 
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        Long = trip_details['lon'][0],
        Lat = trip_details['lat'][0],
        my_test = execution_counter,
        sun_posi = sun_list,
        origin_name = user_origin,
        destination_name = user_destination,
        execution_counter = execution_counter,
        geojson_input = coords_list #needs to be geojson form or list of lists i think 
    )
def get_user_trip_details():
    data = request.get_json()
    return data

@app.route('/getters', methods=['POST','GET'])
def getters():
    print("ive been called from getters")
    global execution_counter
    print(execution_counter)
   
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json()['time'])  # parse as JSON
        #print("ummmmmmmmmm")
        session['my_var'] = request.get_json()['time']
        return redirect(url_for('mapbox_gl'))

    # GET request
    else:
        message = {'greeting': execution_counter}
        return jsonify(message)  # serialize and use JSON headers


@app.route('/load_fresh', methods=['POST','GET'])
def load_refresh():
    print("I've been called because everything has loaded and we want to refresh page")

    val = session.get('reload_val')
    user_time = session.get('my_var', None)
    print(val)
    message = {'reload': val, 'time':user_time}

    print(message)
    return jsonify(message)



    

