Got it — you want **one single, clean Markdown file** with no broken fences. Here is the corrected README as **one proper `.md` file**, ready to paste directly into `README.md`:

````md
# Content-Based Subscriptions on Google Cloud Pub/Sub

This project implements **content-based message filtering** on top of Google Cloud Pub/Sub. Since Pub/Sub natively supports topic-based routing only, subscribers receive all messages and apply **regex-based rules locally** to decide which messages to process. The system also supports **dynamic rule reloading at runtime** without restarting subscribers.

## Features
- Content-based filtering using regular expressions  
- Multiple independent subscribers with different rules  
- Dynamic rule reloading without restarts  
- Automated setup and teardown of Pub/Sub resources  
- Publisher that streams log data from a CSV file  

## Architecture
- **Publisher:** Reads entries from `logs.csv` and publishes messages at a fixed interval  
- **Subscribers (4):** Consume all messages and filter them using regex rules  
- **Automation:** `script.sh` manages topic and subscription lifecycle  

## Requirements
- Google Cloud account with Pub/Sub enabled  
- Python 3.x  
- `gcloud` CLI configured and authenticated  

## Setup

### 1) Clean existing resources
```bash
./script.sh teardown
````

### 2) Create topics and subscriptions

```bash
./script.sh setup
```

## Running the Project

### Start the Publisher

```bash
python3 publisher.py
```

Publishes entries from `logs.csv` every 2 seconds.

### Start a Subscriber (example)

```bash
python3 subscriber_0.py
```

You can also run:

```bash
python3 subscriber_1.py
python3 subscriber_2.py
python3 subscriber_3.py
```

## Rule Management

Subscribers load regex rules from their configuration and can **reload rules at runtime** without restarting. This allows changing filtering logic dynamically while the system is running.

## Project Structure

```text
.
├── publisher.py
├── subscriber_0.py
├── subscriber_1.py
├── subscriber_2.py
├── subscriber_3.py
├── logs.csv
├── script.sh
└── sample_output/
```

## Automation

`script.sh` provides:

* **setup:** creates Pub/Sub topics and subscriptions
* **teardown:** deletes all project resources

## Use Cases

* Event routing based on message content
* Log stream filtering
* Prototyping content-aware messaging in cloud systems

## Author

**Rufat Hajizada**