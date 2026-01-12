import json
import yaml
import time
import re
import threading
from google.cloud import pubsub_v1

PROJECT_ID = "inft-3507-hw2"
TOPIC_SUFFIX = "rhajizada"
SUBSCRIBER_ID = "0"
RULES_FILE = "../rules.json"
RELOAD_INTERVAL = 10

subscriber = pubsub_v1.SubscriberClient()

SUBSCRIPTIONS = {
    "INFO": f"projects/{PROJECT_ID}/subscriptions/sub-{SUBSCRIBER_ID}-INFO-{TOPIC_SUFFIX}",
    "DEBUG": f"projects/{PROJECT_ID}/subscriptions/sub-{SUBSCRIBER_ID}-DEBUG-{TOPIC_SUFFIX}",
    "WARN": f"projects/{PROJECT_ID}/subscriptions/sub-{SUBSCRIBER_ID}-WARN-{TOPIC_SUFFIX}",
    "ERROR": f"projects/{PROJECT_ID}/subscriptions/sub-{SUBSCRIBER_ID}-ERROR-{TOPIC_SUFFIX}",
    "ALERT": f"projects/{PROJECT_ID}/subscriptions/sub-{SUBSCRIBER_ID}-ALERT-{TOPIC_SUFFIX}",
}

rules = []
rules_lock = threading.Lock()

def load_rules():
    if RULES_FILE.endswith(".json"):
        with open(RULES_FILE) as f:
            data = json.load(f)
    else:
        with open(RULES_FILE) as f:
            data = yaml.safe_load(f)

    compiled = []
    for r in data["subscribers"][SUBSCRIBER_ID]:
        compiled.append({
            "level": r["level"],
            "pattern": re.compile(r["pattern"])
        })

    with rules_lock:
        rules.clear()
        rules.extend(compiled)

    print(f"[RULES RELOADED] Subscriber {SUBSCRIBER_ID}")

def rule_reloader():
    while True:
        load_rules()
        time.sleep(RELOAD_INTERVAL)

def callback(message, level):
    text = message.data.decode("utf-8")

    with rules_lock:
        active_rules = list(rules)

    for r in active_rules:
        if r["level"] == level and r["pattern"].search(text):
            print(f"[SUB {SUBSCRIBER_ID} MATCH] ({level}) {text}")
            break

    message.ack()

def listen():
    threading.Thread(target=rule_reloader, daemon=True).start()

    for level, sub_path in SUBSCRIPTIONS.items():
        subscriber.subscribe(
            sub_path,
            callback=lambda msg, lvl=level: callback(msg, lvl)
        )

    print(f"Subscriber {SUBSCRIBER_ID} listening...")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    listen()
