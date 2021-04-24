from flask import Flask, request, abort
from token_key import YOUR_CHANNEL_SECRET, YOUR_CHANNEL_ACCESS_TOKEN

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage, TemplateSendMessage, TemplateSendMessage, ButtonsTemplate, URIAction
)

app = Flask(__name__)
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def main():
    messages = TextSendMessage(text="今日も世界遺産を勉強しましょう！")
    line_bot_api.broadcast(messages=messages)

if __name__=="__main__":
    main()