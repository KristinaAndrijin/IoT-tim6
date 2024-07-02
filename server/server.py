import math
import threading
import time
from datetime import datetime

from flask import Flask, jsonify, request, render_template, g, current_app
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit
import json
import os
from globals import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# InfluxDB Configuration
# token = "ro0VzFsPfBwi966JZz2GaDO7_eYZ3qbS0ST-5FcL1Cy1Otsm7u6EUTULZ63vAZ21uZOztAhpWX9SymeXsRkpxQ==" # Vlada
token = "SQuqGj-Pi9okHh4f8trKHhVU2hXORmzyw207p1vBC9p16zrUS_WVOfYGhkz_8cRD7D9qmERBtln_TRS6rYzJGA=="  # Kris
org = "FTN"
url = "http://localhost:8086"
bucket = "example_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

dus1_new_readings = 0
dus2_new_readings = 0
should_check_dus1 = False
should_check_dus2 = False
num_of_people = 0
last_ds1 = False
last_ds2 = False




def on_connect(client, userdata, flags, rc):
    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("Door opened")
    client.subscribe("Combination")
    client.subscribe("Distance")
    client.subscribe("Motion")
    client.subscribe("Door Buzzer")
    client.subscribe("LightState")
    client.subscribe("Acceleration")
    client.subscribe("Gyro")
    client.subscribe("IrReading")
    client.subscribe("RGBState")
    client.subscribe("setup")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: process_the_message(msg.topic,
                                                                           json.loads(msg.payload.decode('utf-8')))


def process_the_message(topic, data):
    if topic == "setup":
        print(data)
        transformed_data = transform_setup_data(data)
        print(transformed_data)
        send_setup_to_angular(transformed_data)
    else:
        save_to_db(data)
        with app.app_context():
            check_for_triggers(data)
        send_values_to_angular(data)

def turn_on_security(data):
    set_security_system_activated(True)
    check_code(data['value'])

def check_for_triggers(data):
    code = data["code"]
    try:
        if code == "DPIR1 - Covered Porch":
            handle_dpir1(data)

        if code == "DPIR2 - Garage":
            handle_dpir2(data)

        global dus1_new_readings, should_check_dus1, num_of_people
        if code == "DUS1 - Covered Porch" and should_check_dus1:
            if dus1_new_readings > 1:
                handle_dus(1)
                should_check_dus1 = False
                dus1_new_readings = 0
            else:
                dus1_new_readings += 1

        global dus2_new_readings, should_check_dus2
        if code == "DUS2 - Garage" and should_check_dus2:
            if dus2_new_readings > 1:
                handle_dus(2)
                should_check_dus2 = False
                dus2_new_readings = 0
            else:
                dus2_new_readings += 1

        if code == "DS1 - Foyer":
            handle_ds(1)
            handle_ds_dms(data)
        elif code == "DS2 - Family Foyer":
            handle_ds(2)
            handle_ds_dms(data)

        if code == "DMS - Foyer":
            timer = threading.Timer(10.0, turn_on_security, args=(data,))
            timer.start()
            if is_dms_alarm_raised():
                handle_dms_code(data['value'])

        if code == "RPIR1 - Bedroom Doors" or code == "RPIR2 - Open railing" or "RPIR3 - Kitchen" or "RPIR4 - Dinette":
            handle_rpir(data['value'])

        if code == "GSG - Gun Safe Gyro":
            handle_gsg(data)

    except Exception as e:
        print(f"Error in check_for_triggers: {str(e)}")


def handle_dpir1(data):
    if data["value"] is True:

        global num_of_people,should_check_dus1

        # Provera da li neko ulazi
        should_check_dus1 = True

        query = f"""
                from(bucket: "example_db")
                  |> range(start: -10m, stop: now())
                  |> filter(fn: (r) => r["_measurement"] == "Distance")
                  |> filter(fn: (r) => r["_field"] == "measurement")
                  |> filter(fn: (r) => r["code"] == "DUS1 - Covered Porch")
                  |> sort(columns: ["_time"], desc: true)
                  |> limit(n: 3)
                  |> yield(name: "dus1")
        """

        print("dpir1 zove")
        influx_data = handle_influx_query(query)


        if influx_data["status"] == "success":
            points = influx_data["data"]
            print(points)

            if len(points) == 3:
                if points[0] > points[1] > points[2]:
                    if (num_of_people > 0):
                        print("Detektovane opadajuce vrednosti, neko izlazi.")
                        num_of_people -= 1
                        send_number_of_people()
                        print("broj ljudi je", num_of_people)

        else:
            print(f"InfluxDB query failed: {influx_data['message']}")



def handle_dpir2(data):
    if data["value"] is True:

        global num_of_people,should_check_dus2

        # provera da li neko ulazi
        should_check_dus2 = True

        query = f"""
                    from(bucket: "example_db")
                      |> range(start: -10m, stop: now())
                      |> filter(fn: (r) => r["_measurement"] == "Distance")
                      |> filter(fn: (r) => r["_field"] == "measurement")
                      |> filter(fn: (r) => r["code"] == "DUS2 - Garage")
                      |> sort(columns: ["_time"], desc: true)
                      |> limit(n: 3)
                      |> yield(name: "dus2")
                """
        print("dpir2 zove")
        influx_data = handle_influx_query(query)

        if influx_data["status"] == "success":
            points = influx_data["data"]
            print(points)
            if len(points) == 3:

                if points[0] > points[1] > points[2]:
                    if (num_of_people > 0):
                        print("Detektovane opadajuce vrednosti, neko izlazi.")
                        num_of_people -= 1
                        send_number_of_people()
                        print("broj ljudi je", num_of_people)

        else:
            print(f"InfluxDB query failed: {influx_data['message']}")

def handle_dus(number):


        global num_of_people
        query = f"""
                           from(bucket: "example_db")
                             |> range(start: -10m, stop: now())
                             |> filter(fn: (r) => r["_measurement"] == "Distance")
                             |> filter(fn: (r) => r["_field"] == "measurement")
                             |> filter(fn: (r) => r["code"] == "DUS1 - Covered Porch")
                             |> sort(columns: ["_time"], desc: true)
                             |> limit(n: 3)
                             |> yield(name: "dus1")
                   """
        if number == 2:
            query = f"""
                           from(bucket: "example_db")
                             |> range(start: -10m, stop: now())
                             |> filter(fn: (r) => r["_measurement"] == "Distance")
                             |> filter(fn: (r) => r["_field"] == "measurement")
                             |> filter(fn: (r) => r["code"] == "DUS2 - Garage")
                             |> sort(columns: ["_time"], desc: true)
                             |> limit(n: 3)
                             |> yield(name: "dus2")
                   """
        print("dus"+str(number)+" zove")
        influx_data = handle_influx_query(query)

        if influx_data["status"] == "success":
            points = influx_data["data"]
            print(points)
            if len(points) == 3:
                pass

                if points[0] < points[1] < points[2]:
                    print("Detektovane rastuce vrednosti, neko ulazi.")
                    num_of_people += 1
                    send_number_of_people()
                    print("broj ljudi je", num_of_people)


def handle_ds(ds_type):
    global last_ds1, last_ds2
    query = ""
    if (ds_type == 1):
        query = f"""
                   from(bucket: "example_db")
                     |> range(start: -5s, stop: now())
                     |> filter(fn: (r) => r["_measurement"] == "Door opened")
                     |> filter(fn: (r) => r["_field"] == "measurement")
                     |> filter(fn: (r) => r["code"] == "DS1 - Foyer")
                     |> sort(columns: ["_time"], desc: true)
                     |> yield(name: "ds1")
                """
    else:
        query = f"""
                   from(bucket: "example_db")
                     |> range(start: -5s, stop: now())
                     |> filter(fn: (r) => r["_measurement"] == "Door opened")
                     |> filter(fn: (r) => r["_field"] == "measurement")
                     |> filter(fn: (r) => r["code"] == "DS2 - Family Foyer")
                     |> sort(columns: ["_time"], desc: true)
                     |> yield(name: "ds2")
                """
    influx_data = handle_influx_query(query)

    if influx_data["status"] == "success":
        points = influx_data["data"]
        print(points)

        if False in points and ((last_ds1 and ds_type == 1) or (last_ds2 and ds_type == 2)):
            print("STOP ALARM")
            payload = {
                "ds": ds_type
            }
            json_payload = json.dumps(payload)
            mqtt_client.publish("turn_alarm_off_ds_pi1", json_payload)
            mqtt_client.publish("turn_alarm_off_ds_pi3", json_payload)
            if ds_type == 1:
                last_ds1 = False
            else:
                last_ds2 = False

        should_raise_alarm = all(points)
        if should_raise_alarm:
            print("ALARM! DS")
            payload = {
                "ds": ds_type
            }
            json_payload = json.dumps(payload)
            mqtt_client.publish("raise_alarm_ds_pi1", json_payload)
            mqtt_client.publish("raise_alarm_ds_pi3", json_payload)

            if ds_type == 1:
                last_ds1 = True
            else:
                last_ds2 = True


def handle_ds_dms(data):
    print("DMS DS")
    if is_dms_alarm_raised():
        return
    if data['value'] and (not is_code_correct()) and is_security_system_active(): # ako ima signala na DS
        set_dms_is_alarm_raised(True)
        print("DMS ALARM")
        payload = {
            "ds": data['code']
        }
        json_payload = json.dumps(payload)
        mqtt_client.publish("raise_alarm_dms_ds_pi1", json_payload)
        mqtt_client.publish("raise_alarm_dms_ds_pi3", json_payload)


def handle_dms_code(code):
    print(code)
    check_code(code)
    if is_code_correct():
        set_dms_is_alarm_raised(False)
        payload = {
            "code": code
        }
        json_payload = json.dumps(payload)
        mqtt_client.publish("turn_off_alarm_dms_ds_pi1", json_payload)
        mqtt_client.publish("turn_off_alarm_dms_ds_pi3", json_payload)


def handle_rpir(signal):
    if signal and num_of_people == 0:
        print("RPIR")
        payload = {
            "alarm": True
        }
        json_payload = json.dumps(payload)
        mqtt_client.publish("raise_alarm_rpir_pi1", json_payload)
        mqtt_client.publish("raise_alarm_rpir_pi3", json_payload)
        set_rpir_alarm_raised(True)


def calculate_magnitude(x, y, z):
    return math.sqrt(x ** 2 + y ** 2 + z ** 2)

def handle_gsg(data):
    print("GYROOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    value = data['value'].split(',')
    if data['measurement'] == 'Acceleration':
        accel_magnitude = calculate_magnitude(float(value[0]), float(value[1]), float(value[2]))
        if accel_magnitude > get_acc_threshold():
            print("ALARM ACC " + str(accel_magnitude))
            set_gyro_alarm_raised(True)
            payload = {
                "acc": accel_magnitude
            }
            json_payload = json.dumps(payload)
            mqtt_client.publish("raise_alarm_gyro_pi1", json_payload)
            mqtt_client.publish("raise_alarm_gyro_pi3", json_payload)
    if data['measurement'] == 'Gyro':
        gyro_magnitude = calculate_magnitude(float(value[0]), float(value[1]), float(value[2]))
        if gyro_magnitude > get_gyro_threshold():
            print("ALARM ROT " + str(gyro_magnitude))
            set_gyro_alarm_raised(True)
            payload = {
                "gyro": gyro_magnitude
            }
            json_payload = json.dumps(payload)
            mqtt_client.publish("raise_alarm_gyro_pi1", json_payload)
            mqtt_client.publish("raise_alarm_gyro_pi3", json_payload)

def send_number_of_people():
    print("šaljem",num_of_people)
    payload = {
        "n_people": num_of_people
    }
    json_payload = json.dumps(payload)
    mqtt_client.publish("n_people", json_payload)

def send_rgb_values(rgb):
    print("šaljem",rgb)
    payload = {
        "rgb": rgb
    }
    json_payload = json.dumps(payload)
    mqtt_client.publish("rgb", json_payload)

def send_timer_value(time):
    print("šaljem",time)
    payload = {
        "time": time
    }
    json_payload = json.dumps(payload)
    mqtt_client.publish("set_timer", json_payload)

def send_timer_turnoff():
    print("šaljem turnoff za timer")
    payload = {
        "state": False
    }
    json_payload = json.dumps(payload)
    mqtt_client.publish("timer_off", json_payload)

def transform_setup_data(data):
    pi_name = data.get("pi_name", "")
    transformed_data = []
    for device_code, device_info in data.get("devices", {}).items():
        device_name = device_info.get("code", "")
        simulated = device_info.get("simulated", False)
        transformed_data.append({"name": device_name, "simulated": simulated})
    final_data = {"pi_name": pi_name, "devices": transformed_data}

    return final_data


def send_setup_to_angular(transformed_data):
    try:
        socketio.emit("angular_setup", transformed_data, namespace='/angular')
        print("Setup data sent to Angular via Websockets")
    except Exception as e:
        print(f"Error sending data to Angular: {str(e)}")


def send_values_to_angular(data):
    try:
        socketio.emit("values", data, namespace='/angular')
        # print("Data sent to Angular via Websockets")
    except Exception as e:
        print(f"Error sending data to Angular: {str(e)}")


def save_to_db(data):
    #print('zdravooo, snimanje na db')
    print(data)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("code", data["code"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


# Route to store dummy data
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values["_value"])
        return {"status": "success", "data": container}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@socketio.on('connect', namespace='/angular')
def handle_connect():
    print('Client connected to Angular')


@socketio.on('disconnect', namespace='/angular')
def handle_disconnect():
    print('Client disconnected from Angular')


@socketio.on('set_rgb', namespace='/angular')
def handle_set_rgb(data):
    try:
        rgb_values = data['rgb']
        print("Received RGB values:", rgb_values)
        send_rgb_values(rgb_values)
    except Exception as e:
        print(f"Error handling set_rgb event: {str(e)}")

@socketio.on('set_timer', namespace='/angular')
def handle_set_timer(data):
    try:
        date_time = data['time']
        print("Received timer datetime:", date_time)
        #parsed_datetime = datetime.fromisoformat(date_time.replace('Z', '+00:00'))
        send_timer_value(date_time)
        #print("xdxdxdxd     tip",type(parsed_datetime))
    except Exception as e:
        print(f"Error handling set_rgb event: {str(e)}")

@socketio.on('turn_off_timer', namespace='/angular')
def handle_turn_off_timer():
    try:
        send_timer_turnoff()
        print("Received timer turn off message:")
    except Exception as e:
        print(f"Error handling set_rgb event: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

