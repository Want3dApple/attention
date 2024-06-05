from flask import Flask, render_template, request, send_from_directory, jsonify
from pywebpush import webpush, WebPushException
import json

app = Flask(__name__)
app.secret_key = '1234'  # Necessary for flashing messages

HOST_NAME = "localhost"
HOST_PORT = 5000
VAPID_PRIVATE_KEY = "Ze_D4hOA2VsbG4TDv2CpHuVowpS27q--xNJkD6Or3Go"
VAPID_PUBLIC_KEY = "BLUCJpm7j7aQ-OkrXvlJwYbLSvlcmrw5BY_YKJ_mBlZSNTQkKXzicuXdfmCAnjuWDc2azHTVQKA1eFqBTad1y-U"
VAPID_SUBJECT = "mailto:want3spam@email.com"
#VAPID_CLAIMS = {
#    "sub": "want3spam@gmail.com"
#}

# In-memory list of subscriptions
subscriptions = []

@app.route('/')
def index():
    return render_template('index.html', public_key=VAPID_PUBLIC_KEY)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    subscription = request.get_json()
    subscriptions.append(subscription)
    return jsonify(subscription)

@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = json.dumps({
        "title": "Gib!",
        "body": "Gib",
        "icon": "static/i-ico.png",
        "image": "static/i-banner.png"
    })
    for subscription in subscriptions:
        send_push_message(subscription, data)
    return "Notification sent to all subscribers!"

def send_push_message(subscription, data):
    try:
        webpush(
            subscription_info=subscription,
            data=data,
            vapid_private_key=VAPID_PRIVATE_KEY,
            #vapid_claims=VAPID_CLAIMS
        )
        print(f"Sent message to {subscription['endpoint']}")
    except WebPushException as ex:
        print(f"Failed to send message to {subscription['endpoint']}: {ex}")

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js')

if __name__ == '__main__':
    app.run(debug=True, host=HOST_NAME, port=HOST_PORT)