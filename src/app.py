from flask import Flask, request, abort
from token_key import YOUR_CHANNEL_SECRET, YOUR_CHANNEL_ACCESS_TOKEN

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from youtube import youtubesearch
from wiki import get_description
from randomselect import select
app = Flask(__name__)
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)#そのメッセージがどんなタイプか確認、signture
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    query = select(event.message.text)
    wiki_description = get_description(query)
    youtube_url = youtubesearch(query)
    app.logger.debug(wiki_description)
    app.logger.debug(youtube_url)

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=wiki_description),
        TextSendMessage(text=youtube_url)])


if __name__ == "__main__":
    app.run(debug=True)
