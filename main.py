from flask import Flask, request
from mattermost import open_dialog, send_message

app = Flask(__name__)

@app.route('/post', methods=["POST"])
def send_mes():
    request_data = request.get_json()
    return send_message(request_data)

@app.route('/form', methods=["POST"])
def form():
    request_data = str(request.form.getlist("trigger_id")).replace("['", "").replace("']", "")
    return open_dialog(request_data)

if __name__ == '__main__':
    app.run(port='3333', host='127.0.0.1')
