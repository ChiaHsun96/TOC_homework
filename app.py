import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent
from fsm import TocMachine
from fsm import *
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["dummy","menu", "time_county", "time", "push_notify","weather","weather_county","show_picture"],
    transitions=[
        {
            "trigger": "advance",
            "source": "dummy",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "time_county",
            "conditions": "is_going_to_time_county",
        },
        {
            "trigger": "advance",
            "source": "time_county",
            "dest": "menu",
            "conditions": "time_county_back_menu",
        },
        {
            "trigger": "advance",
            "source": "time_county",
            "dest": "time",
            "conditions": "is_going_to_time",
        },
        {
            "trigger": "advance",
            "source": "time",
            "dest": "time_county",
            "conditions": "time_back_time_county",
        },
        {
            "trigger": "advance",
            "source": "time",
            "dest": "menu",
            "conditions": "time_back_menu",
        },
        {
            "trigger": "advance",
            "source": "time",
            "dest": "push_notify",
            "conditions": "is_going_to_push_notify",
        },
        {
            "trigger": "advance",
            "source": "push_notify",
            "dest": "menu",
            "conditions": "push_notify_back_menu",
        },
        {
            "trigger": "advance",
            "source": "push_notify",
            "dest": "time_county",
            "conditions": "push_notify_back_time_county",
        },
        {
            "trigger": "advance",
            "source": "push_notify",
            "dest": "time",
            "conditions": "push_notify_back_time",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "weather",
            "conditions": "is_going_to_weather",
        },
        {
            "trigger": "advance",
            "source": "weather",
            "dest": "menu",
            "conditions": "weather_back_menu",
        },
        {
            "trigger": "advance",
            "source": "weather",
            "dest": "weather_county",
            "conditions": "is_going_to_weather_county",
        },
        {
            "trigger": "advance",
            "source": "weather_county",
            "dest": "weather",
            "conditions": "weather_county_back_weather",
        },
        {
            "trigger": "advance",
            "source": "weather_county",
            "dest": "menu",
            "conditions": "weather_county_back_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "show_picture",
            "conditions": "is_going_to_show_picture",
        },
        {
            "trigger": "advance",
            "source": "show_picture",
            "dest": "menu",
            "conditions": "show_picture_back_menu",
        },
    ],
    initial="dummy",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if isinstance(event, PostbackEvent):
            print(f"\nFSM STATE: {machine.state}")
            print(f"REQUEST BODY: \n{body}")
            response = machine.advance(event)
            return "OK"
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "無此資料,請重新輸入")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
