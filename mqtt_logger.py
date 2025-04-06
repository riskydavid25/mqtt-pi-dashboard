import paho.mqtt.client as mqtt
import json
import csv
import os
from datetime import datetime

# Konfigurasi MQTT
BROKER = "broker.emqx.io"
PORT = 1883
SENDERS = ["sender1", "sender2", "sender3"]
TOPICS = [(f"waitress/{sender}/call", 1) for sender in SENDERS] + \
         [(f"waitress/{sender}/bill", 1) for sender in SENDERS]
CLIENT_ID = "PythonSubscriberMulti"
CSV_FILE = "mqtt_log_multi.csv"

# Header CSV
CSV_HEADER = ["timestamp_received", "topic", "sender_id", "type", "status", "count", "rssi", "timestamp_sent"]

# Buat file CSV jika belum ada
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADER)

# Callback saat terhubung
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        client.subscribe(TOPICS)
        print(f"📡 Subscribed to topics: {[t[0] for t in TOPICS]}")
    else:
        print(f"❌ Failed to connect, return code {rc}")

# Callback saat pesan diterima
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        timestamp_received = datetime.now().isoformat()

        # Parsing id dari payload
        sender_id = data.get("id", "Unknown")
        data_type = data.get("type", "")
        status = data.get("status", "")
        count = data.get("count", "")
        rssi = data.get("rssi", "")
        timestamp_sent = data.get("timestamp", "")

        row = [
            timestamp_received,
            msg.topic,
            sender_id,
            data_type,
            status,
            count,
            rssi,
            timestamp_sent
        ]

        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)

        print(f"📝 [{sender_id}] Logged from topic {msg.topic}")

    except json.JSONDecodeError:
        print(f"⚠️ JSON Decode Error from topic {msg.topic}: {msg.payload}")

# Setup MQTT Client
client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
