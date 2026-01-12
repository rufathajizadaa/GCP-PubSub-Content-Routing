import csv
import time
from google.cloud import pubsub_v1

PROJECT_ID = "inft-3507-hw2"
TOPIC_SUFFIX = "rhajizada"

publisher = pubsub_v1.PublisherClient()

TOPICS = {
    "INFO": f"projects/{PROJECT_ID}/topics/INFO-{TOPIC_SUFFIX}",
    "DEBUG": f"projects/{PROJECT_ID}/topics/DEBUG-{TOPIC_SUFFIX}",
    "WARN": f"projects/{PROJECT_ID}/topics/WARN-{TOPIC_SUFFIX}",
    "ERROR": f"projects/{PROJECT_ID}/topics/ERROR-{TOPIC_SUFFIX}",
    "ALERT": f"projects/{PROJECT_ID}/topics/ALERT-{TOPIC_SUFFIX}",
}

def publish_logs():
    while True:
        with open("logs.csv", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                level = row["level"]
                message = row["message"]

                topic_path = TOPICS[level]
                publisher.publish(topic_path, message.encode("utf-8"))

                print(f"[PUBLISHED → {level}] {message}")
                time.sleep(2)

if __name__ == "__main__":
    publish_logs()
