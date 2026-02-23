from flask import Flask, request, jsonify
from datetime import datetime, timezone
from flask import render_template
from pymongo import MongoClient
mongo_uri = "mongodb+srv://suchita:Suchita123@cluster0.5tfhfcl.mongodb.net/github_webhooks?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client["github_webhooks"]
collection = db["events"]
client = MongoClient(mongo_uri)

db = client["github_webhooks"]
collection = db["events"]

# Flask app instance
app = Flask(__name__)

@app.route("/")
def home():
    return "Webhook Server is Running 🚀"


@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event_type == "push":
        author = payload["head_commit"]["author"]["name"]

        # Extract branch
        ref = payload["ref"]
        to_branch = ref.split("/")[-1]

        # Extract original timestamp
        raw_timestamp = payload["head_commit"]["timestamp"]

        # Convert to datetime object (auto parses timezone)
        dt_object = datetime.fromisoformat(raw_timestamp)

        # Convert to UTC
        dt_utc = dt_object.astimezone(timezone.utc)

        # Format nicely
        formatted_timestamp = dt_utc.strftime("%d %B %Y - %I:%M %p UTC")
        document = {
            "request_id": payload["head_commit"]["id"],
            "author": author,
            "action": "PUSH",
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": dt_utc
        }

        collection.insert_one(document)

        print("Inserted into MongoDB")
        print("Author:", author)
        print("Branch:", to_branch)
        print("UTC Timestamp:", formatted_timestamp)
    
    elif event_type == "pull_request":
        action = payload["action"]

        # Only handle opened pull requests
        if action == "opened":
            author = payload["pull_request"]["user"]["login"]

            from_branch = payload["pull_request"]["head"]["ref"]
            to_branch = payload["pull_request"]["base"]["ref"]

            raw_timestamp = payload["pull_request"]["created_at"]
            dt_object = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00"))
            dt_utc = dt_object.astimezone(timezone.utc)

            document = {
                "request_id": payload["pull_request"]["id"],
                "author": author,
                "action": "PULL_REQUEST",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": dt_utc
            }

            collection.insert_one(document)

            print("Pull Request Inserted into MongoDB")

        elif action == "closed" and payload["pull_request"]["merged"] is True:
            author = payload["pull_request"]["user"]["login"]
            from_branch = payload["pull_request"]["head"]["ref"]
            to_branch = payload["pull_request"]["base"]["ref"]

            raw_timestamp = payload["pull_request"]["merged_at"]
            dt_object = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00"))
            dt_utc = dt_object.astimezone(timezone.utc)

            document = {
                "request_id": payload["pull_request"]["id"],
                "author": author,
                "action": "MERGE",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": dt_utc
            }

            collection.insert_one(document)

            print("Merge Event Inserted into MongoDB")

    return jsonify({"message": "Webhook received successfully"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("timestamp", -1))

    result = []

    for event in events:
        if event["action"] == "PUSH":
            message = f'{event["author"]} pushed to {event["to_branch"]} on {event["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")}'

        elif event["action"] == "PULL_REQUEST":
            message = f'{event["author"]} submitted a pull request from {event["from_branch"]} to {event["to_branch"]} on {event["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")}'

        elif event["action"] == "MERGE":
            message = f'{event["author"]} merged branch {event["from_branch"]} to {event["to_branch"]} on {event["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")}'

        result.append({
            "message": message
        })

    return jsonify(result)

@app.route("/ui")
def ui():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)