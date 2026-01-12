#!/bin/bash

PROJECT_ID="inft-3507-hw2"
SUFFIX="rhajizada"

TOPICS=("INFO" "DEBUG" "WARN" "ERROR" "ALERT")
SUBSCRIBERS=(0 1 2 3)

echo "Using project: $PROJECT_ID"

if [ "$1" == "setup" ]; then
  echo "Setting up Pub/Sub topics and subscriptions..."

  for topic in "${TOPICS[@]}"; do
    if gcloud pubsub topics describe "${topic}-${SUFFIX}" >/dev/null 2>&1; then
      echo "Topic ${topic}-${SUFFIX} already exists. Skipping."
    else
      gcloud pubsub topics create "${topic}-${SUFFIX}"
      echo "Created topic ${topic}-${SUFFIX}"
    fi
  done

  for sub in "${SUBSCRIBERS[@]}"; do
    for topic in "${TOPICS[@]}"; do
      SUB_NAME="sub-${sub}-${topic}-${SUFFIX}"
      TOPIC_NAME="${topic}-${SUFFIX}"

      if gcloud pubsub subscriptions describe "$SUB_NAME" >/dev/null 2>&1; then
        echo "Subscription $SUB_NAME already exists. Skipping."
      else
        gcloud pubsub subscriptions create "$SUB_NAME" --topic="$TOPIC_NAME"
        echo "Created subscription $SUB_NAME"
      fi
    done
  done

  echo "Setup completed."

elif [ "$1" == "teardown" ]; then
  echo "Tearing down Pub/Sub subscriptions and topics..."

  for sub in "${SUBSCRIBERS[@]}"; do
    for topic in "${TOPICS[@]}"; do
      SUB_NAME="sub-${sub}-${topic}-${SUFFIX}"
      gcloud pubsub subscriptions delete "$SUB_NAME" --quiet
    done
  done

  for topic in "${TOPICS[@]}"; do
    gcloud pubsub topics delete "${topic}-${SUFFIX}" --quiet
  done

  echo "Teardown completed."

else
  echo "Usage: ./script.sh setup | teardown"
fi
