import datetime
from flask import Flask, request
from mattermost import open_dialog, send_message

app = Flask(__name__)

@app.route('/post', methods=["POST"])
def send_mes():
    request_data = request.get_json()
    return send_message(request_data)

@app.route('/form', methods=["POST"])
def form():
    trigger_id = str(request.form.getlist("trigger_id")).replace("['", "").replace("']", "")
    user_name = str(request.form.getlist("user_name")).replace("['", "").replace("']", "")
    channel_name = str(request.form.getlist("channel_name")).replace("['", "").replace("']", "")
    print(str(datetime.datetime.now()) + ": User '" + user_name + "' executed slash-command in channel '" + channel_name + "'")
    return open_dialog(trigger_id)

if __name__ == '__main__':
    app.run(port='3333', host='127.0.0.1')
