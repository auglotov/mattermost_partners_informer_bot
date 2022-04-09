import json
import flask
import requests
import datetime
from settings import MM_BOT_TOKEN, MM_API_URL, MM_HOOK_URL, PY_BOT_URL, ICON_URL, CHANNELS

def open_dialog(trigger_id):
    dialog = {
        "callback_id": "partners_informer",
        "title": "Partners informer",
        "icon_url": ICON_URL,
        "elements": [
            {
                "display_name": "Выбери тип инцидента",
                "name": "incident_type",
                "type": "select",
                "subtype": "",
                "default": "",
                "placeholder": "Тип инцидента...",
                "help_text": "",
                "optional": False,
                "min_length": 0,
                "max_length": 0,
                "data_source": "",
                "options": [
                    {
                        "text": "Недоступность",
                        "value": ":alert_red:"
                    },
                    {
                        "text": "Деградация",
                        "value": ":fire:"
                    },
                    {
                        "text": "Плановые рабты",
                        "value": ":warning:"
                    },
                    {
                        "text": "Работа восстановлена",
                        "value": ":white_check_mark:"
                    }
                ]
            },
            {
                "display_name": "Укажи, в какой системе ошибка",
                "name": "system_name",
                "type": "text",
                "subtype": "",
                "default": "",
                "placeholder": "Система...",
                "help_text": "",
                "optional": False,
                "min_length": 0,
                "max_length": 0,
                "data_source": "",
                "options": None
            },
            {
                "display_name": "Опиши проблему",
                "name": "problem_type",
                "type": "text",
                "subtype": "",
                "default": "",
                "placeholder": "Проблема...",
                "help_text": "",
                "optional": False,
                "min_length": 0,
                "max_length": 0,
                "data_source": "",
                "options": None
            },
            {
                "display_name": "Укажи примерное время восстановления",
                "name": "recovery_time",
                "type": "text",
                "subtype": "",
                "default": "",
                "placeholder": "Время восстановления...",
                "help_text": "",
                "optional": False,
                "min_length": 0,
                "max_length": 0,
                "data_source": "",
                "options": None
            }
        ],
        "submit_label": "Отправить",
        "notify_on_cancel": False,
        "state": "somestate"
    }

    payload = {
        'trigger_id': trigger_id,
        'url': PY_BOT_URL + '/post',
        'dialog': dialog
    }

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'authorization': 'Bearer' + MM_BOT_TOKEN
    }

    json_string = json.dumps(payload, indent=4)
    response = requests.post(MM_API_URL + '/actions/dialogs/open', headers=headers, data=json_string)
    print(str(datetime.datetime.now()) + ": Dialog start completed status is " + str(response.status_code))
    return flask.Response(response)


def send_message(request_data):
    user_id = request_data['user_id']
    submission = request_data['submission']
    incident_type = submission['incident_type']
    system_name = submission['system_name']
    problem_type = submission['problem_type']
    recovery_time = submission['recovery_time']

    i = 0
    response = None
    while i < len(CHANNELS):
        payload = {
            'channel': CHANNELS[i],
            'username': 'DEV Support bot',
            'text': (incident_type + '  **' + system_name + '**\n\n:scroll: **Описание:** '
                     + problem_type + '\n:hourglass_flowing_sand: **Примерное время восстановления:** '
                     + recovery_time + '\n:speaking_head_in_silhouette: **Сообщение от:** <@' + user_id + '>')
        }

        headers = {
            'Content-Type': 'application/json'
        }

        json_string = json.dumps(payload, indent=4)
        response = requests.post(MM_HOOK_URL, headers=headers, data=json_string)
        print(str(datetime.datetime.now()) + ": Notification sending status in '" + CHANNELS[i] + "' is " + str(response.status_code))
        i += 1

    return flask.Response(response)
