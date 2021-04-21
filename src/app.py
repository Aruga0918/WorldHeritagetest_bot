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
from youtube import youtubesearch
from wiki import get_description
from randomselect import select
from makequize import Quiz
app = Flask(__name__)
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

quiz = Quiz()
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
    user_id = event.source.user_id
    app.logger.info(user_id)
    if quiz.dictio(user_id):
        if event.message.text == "クイズ":
            button_messages = quiz.sendfinish()
            line_bot_api.reply_message(
                event.reply_token,
                button_messages
                )
    else:
        query = select(event.message.text)
        if query != "no heritage":
            wiki_description = get_description(query)
            youtube_url = youtubesearch(query)
            app.logger.debug(query)
            app.logger.debug(wiki_description)
            app.logger.debug(youtube_url)
            quiz.make_quiz(user_id,query)
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text=wiki_description),
                TextSendMessage(text=youtube_url)])
            return query
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="該当する世界遺産はありません…ごめんなさい"),
                )
    #     else:
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             TextSendMessage(text="クイズと打つとクイズをだすよ！"))
@handler.add(PostbackEvent)
def on_postback(event):
    data = event.postback.data
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=data))

if __name__ == "__main__":
    app.run(debug=True)
