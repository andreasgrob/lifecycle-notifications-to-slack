import os
import json
from flask import Flask, request, jsonify
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = Flask(__name__)

# Load the Slack webhook URL from an environment variable
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader("."))


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Load the template
    template = env.get_template("slack_message_template.j2")

    # Render the template with the data
    slack_message = json.loads(template.render(data))

    response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)

    if response.status_code != 200:
        return (
            jsonify({"status": "failed", "reason": response.text}),
            response.status_code,
        )

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(port=5000)
