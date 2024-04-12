import time

from flask import Flask, jsonify, request, render_template
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# InfluxDB Configuration
token = "ro0VzFsPfBwi966JZz2GaDO7_eYZ3qbS0ST-5FcL1Cy1Otsm7u6EUTULZ63vAZ21uZOztAhpWX9SymeXsRkpxQ==" # Vlada
# token = "SQuqGj-Pi9okHh4f8trKHhVU2hXORmzyw207p1vBC9p16zrUS_WVOfYGhkz_8cRD7D9qmERBtln_TRS6rYzJGA=="  # Kris
org = "FTN"
url = "http://localhost:8086"
bucket = "example_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

pir_expiry_time = None
current_state = "jagode"


def on_connect(client, userdata, flags, rc):
    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("Door opened")
    client.subscribe("Combination")
    client.subscribe("Distance")
    client.subscribe("Motion")
    client.subscribe("Door Buzzer")
    client.subscribe("LightState")
    client.subscribe("setup")  # Subscribe to the "setup" topic


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: process_the_message(msg.topic,
                                                                           json.loads(msg.payload.decode('utf-8')))


def process_the_message(topic, data):
    if topic == "setup":
        print(data)
        transformed_data = transform_setup_data(data)
        print(transformed_data)
        send_to_angular(transformed_data)
    else:
        save_to_db(data)
        check_for_triggers(data)
        send_values_to_angular(data)


def check_for_triggers(data):
    global pir_expiry_time
    # kada dpir1 detektuje pokret, uključiti dl1 na 10 sekundi
    if data["code"] == "DPIR1 - Covered Porch":
        if pir_expiry_time is not None and time.time() < pir_expiry_time:
            print("preskacemo ovo ipak")
        else:
            pir_expiry_time = time.time() + 10
            print("jagode")
            payload = {
                "for": "dl1"
            }
            json_payload = json.dumps(payload)
            mqtt_client.publish("PI1", json_payload)


def transform_setup_data(data):
    pi_name = data.get("pi_name", "")
    transformed_data = []
    for device_code, device_info in data.get("devices", {}).items():
        device_name = device_info.get("code", "")
        simulated = device_info.get("simulated", False)
        transformed_data.append({"name": device_name, "simulated": simulated})
    final_data = {"pi_name": pi_name, "devices": transformed_data}

    return final_data


def send_to_angular(transformed_data):
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
    # print('zdravooo, snimanje na db')
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
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Humidity")"""
    return handle_influx_query(query)


@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Humidity")
    |> mean()"""
    return handle_influx_query(query)

@app.route('/test_mqtt', methods=['POST'])
def send_mqtt_message():
    data = request.json
    topic = data.get('topic')
    message = json.dumps(data.get('message'))
    print(topic, message)

    mqtt_client.publish(topic, message)
    return jsonify({"status": "success", "message": "MQTT message sent successfully"})


# Use the '/angular' namespace for communication with Angular
@socketio.on('connect', namespace='/angular')
def handle_connect():
    print('Client connected to Angular')


@socketio.on('disconnect', namespace='/angular')
def handle_disconnect():
    print('Client disconnected from Angular')

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)
