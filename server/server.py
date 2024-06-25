import time

from flask import Flask, jsonify, request, render_template, g, current_app
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# InfluxDB Configuration
token = "ro0VzFsPfBwi966JZz2GaDO7_eYZ3qbS0ST-5FcL1Cy1Otsm7u6EUTULZ63vAZ21uZOztAhpWX9SymeXsRkpxQ==" # Vlada
#token = "SQuqGj-Pi9okHh4f8trKHhVU2hXORmzyw207p1vBC9p16zrUS_WVOfYGhkz_8cRD7D9qmERBtln_TRS6rYzJGA=="  # Kris
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



def check_for_triggers(data):
    try:
        if data["code"] == "DPIR1 - Covered Porch":
            handle_dpir1(data)

        if data["code"] == "DPIR2 - Garage":
            handle_dpir2(data)

        global dus1_new_readings, should_check_dus1, num_of_people
        if data["code"] == "DUS1 - Covered Porch" and should_check_dus1:
            if dus1_new_readings > 1:
                handle_dus(1)
                should_check_dus1 = False
                dus1_new_readings = 0
            else:
                dus1_new_readings += 1

        global dus2_new_readings, should_check_dus2
        if data["code"] == "DUS2 - Garage" and should_check_dus2:
            if dus2_new_readings > 1:
                handle_dus(2)
                should_check_dus2 = False
                dus2_new_readings = 0
            else:
                dus2_new_readings += 1

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
                    print("broj ljudi je", num_of_people)


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

if __name__ == '__main__':
    app.run(debug=True)

