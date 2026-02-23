# GitHub Webhook Event Tracker

## Overview

This project captures GitHub webhook events (Push, Pull Request, and Merge), stores them in MongoDB Atlas, and displays them in a UI that automatically refreshes every 15 seconds.

The system demonstrates end-to-end webhook ingestion, database storage, and frontend polling.

---

## Features

- Capture **Push** events
- Capture **Pull Request** events
- Capture **Merge** events (Bonus)
- Store structured data in MongoDB Atlas
- Convert timestamps to UTC
- Display formatted messages in a clean UI
- Auto-refresh UI every 15 seconds

---

## Tech Stack

- Python (Flask)
- MongoDB Atlas (Cloud Database)
- GitHub Webhooks
- Ngrok (Webhook tunneling)
- HTML + JavaScript (Polling UI)

---

## Architecture


action-repo (GitHub Events)
↓
GitHub Webhook
↓
Flask Backend (webhook-repo)
↓
MongoDB Atlas
↓
Frontend UI (/ui)


---

## Project Structure


webhook-repo/
│── app.py
│── requirements.txt
│── README.md
│── templates/
│ └── index.html


---

## Setup Instructions

### Clone Repository


git clone <your-webhook-repo-link>
cd webhook-repo


---

### Create Virtual Environment


python -m venv venv
venv\Scripts\activate


---

### Install Dependencies


pip install -r requirements.txt


---

### Configure MongoDB

Create a MongoDB Atlas cluster and database user.

Update the MongoDB connection string inside `app.py`:


mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/github_webhooks?retryWrites=true&w=majority


---

### Run Flask Server


python app.py


Server runs at:


http://127.0.0.1:5000


---

## Expose Webhook Using Ngrok


ngrok http 5000


Copy the HTTPS URL and configure it in:

GitHub → action-repo → Settings → Webhooks

Payload URL:


https://your-ngrok-url/webhook


Content type: `application/json`

---

## API Endpoints

### 🔹 POST `/webhook`
Receives GitHub webhook events.

### 🔹 GET `/events`
Returns formatted event messages from MongoDB.

### 🔹 GET `/ui`
Displays events in browser.
Auto-refreshes every 15 seconds.

---

## Event Format Examples

Push:

Author pushed to main on 23 February 2026 - 05:10 PM UTC


Pull Request:

Author submitted a pull request from feature to main on 23 February 2026 - 05:15 PM UTC


Merge:

Author merged branch feature to main on 23 February 2026 - 05:20 PM UTC


---

## MongoDB Schema

Each event is stored as:


{
request_id: string,
author: string,
action: "PUSH" | "PULL_REQUEST" | "MERGE",
from_branch: string | null,
to_branch: string,
timestamp: datetime (UTC)
}


---

##  Assignment Requirements Covered

- Webhook Integration ✔
- MongoDB Storage ✔
- Proper Date Handling (UTC) ✔
- Push Event Handling ✔
- Pull Request Handling ✔
- Merge Event Handling (Bonus) ✔
- UI Polling Every 15 Seconds ✔

---

## Author

Suchita Rawat