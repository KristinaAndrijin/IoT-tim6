from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json


app = Flask(__name__)

# InfluxDB Configuration
token = "ro0VzFsPfBwi966JZz2GaDO7_eYZ3qbS0ST-5FcL1Cy1Otsm7u6EUTULZ63vAZ21uZOztAhpWX9SymeXsRkpxQ=="
org = "FTN"
url = "http://localhost:8086"
bucket = "example_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

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
mqtt_client.on_message = lambda client, userdata, msg: process_the_message(msg.topic, json.loads(msg.payload.decode('utf-8')))

def process_the_message(topic, data):
    if topic == "setup":
        print(data)
        transformed_data = transform_setup_data(data)
        print(transformed_data)
        send_to_angular(transformed_data)
    else:
        save_to_db(data)

def transform_setup_data(data):
    transformed_data = []
    for device_code, device_info in data.get("devices", {}).items():
        device_name = device_info.get("code", "")
        simulated = device_info.get("simulated", False)
        transformed_data.append({"name": device_name, "simulated": simulated})

    return transformed_data

def send_to_angular(transformed_data):
    try:
        mqtt_topic = "angular_setup"
        mqtt_payload = json.dumps(transformed_data)
        mqtt_client.publish(mqtt_topic, mqtt_payload)
        print("Setup data sent to Angular via MQTT")
    except Exception as e:
        print(f"Error sending data to Angular: {str(e)}")


def save_to_db(data):
    print('zdravooo')
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("code", data["code"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)

# i dont think i used the code below
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


if __name__ == '__main__':
    app.run(debug=True)
