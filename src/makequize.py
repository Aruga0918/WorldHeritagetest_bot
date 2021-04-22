import re
import random
from flask import Flask
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, TemplateSendMessage, ButtonsTemplate, URIAction, PostbackAction, MessageAction
)
import requests
import urllib
from randomselect import randomchoice,right
from collections import defaultdict

app = Flask(__name__)
class Quiz:
    def __init__(self, title_limit=10):
        self.user2answer = defaultdict(
            lambda: {"answer": "", "correct": "", "miss": ""})
        self.title_limit = title_limit
        self.finish = None
        self.heritage = None

    def dictio(self, user_id):
        return self.user2answer[user_id]["answer"]

    def reset(self, user_id):
        self.user2answer[user_id] = {"answer": "", "correct": "", "miss": ""}

    def get_answer(self, user_id, text):
        if self.user2answer[user_id]["answer"]:
            if self.user2answer[user_id]["answer"] == text:#ユーザが正しい答えのとき
                send_messages = TextSendMessage(
                text=self.user2answer[user_id]["correct"]) #correctに入ってる文字列を送信
            else:#ユーザが間違えたとき
                send_messages = TextSendMessage(
                text=self.user2answer[user_id]["miss"])#missに入ってる文字列を送信
            self.reset(user_id)
            return send_messages
        else:
            return None#クイズイベントが発生してないとき

    def set_answer(self, user_id, answer, correct, miss):
        self.user2answer[user_id]["answer"] = answer
        self.user2answer[user_id]["correct"] = correct
        self.user2answer[user_id]["miss"] = miss

    def make_quiz(self, user_id, heritage,  select_option_num=4):
        self.reset(user_id)
        app.logger.info(f"heritage_title:{heritage}")
        keyanswer = right(heritage)
        reply_correct_sentence = '正解！！'
        reply_miss_sentence = f'不正解！！答えは「{keyanswer}」でした！'
        self.set_answer(user_id, keyanswer, reply_correct_sentence,
                        reply_miss_sentence)
        # if select:
        actions = [PostbackAction(
            label=f"{keyanswer}", data=reply_correct_sentence)]
        while len(actions) < select_option_num:
            conterfactual_titile = randomchoice()
            actions.append(PostbackAction(label=f"{conterfactual_titile}",
                                                data=reply_miss_sentence))

        random.shuffle(actions)

            # message = TextSendMessage(text=description)
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url=None,
                title='キーワード クイズ',
                text='さて，この世界遺産と関連のあるキーワードはなんでしょう？',
                actions=actions
                )
            )
        self.finish = buttons_template_message
        self.heritage = heritage
        # else:
        #     assert user_id is not None
        #     return [TextSendMessage(text=description), TextSendMessage(text="Wikipedia 記述クイズ\nさて，上は何の説明でしょう？")]
    def sendfinish(self):
        return self.finish
    def getview(self):
        return self.heritage

# def make_quiz_button_template(heritage):
#     select_option_num = 4
#     # ボタンに入れられる文字が40文字まで
#     # title_limit = 20
#     # while True:
#     #     wiki_title = get_random_title()
#     #     if title_limit < len(wiki_title):
#     #         continue
#     #     description = get_description(wiki_title)
#     #     image_url = get_image_url(wiki_title)
#     #     if description is not None:
#     #         description = delete_target_word(
#     #             delete_braket(description), wiki_title)
#     #         break

#     # url = f"https://ja.wikipedia.org/wiki/{urllib.parse.quote(wiki_title)}"
#     answer = right(heritage)
#     actions = [PostbackAction(
#         label=f"{answer}", data=f'正解！！')]
#     while len(actions) <= select_option_num:
#         conterfactual_titile = randomchoice()
#         actions.append(PostbackAction(label=f"{conterfactual_titile}",
#                                           data=f'不正解！！答えは「{answer}」でした！'))

#     random.shuffle(actions)

#     # message = TextSendMessage(text=description)
#     buttons_template_message = TemplateSendMessage(
#         alt_text='Buttons template',
#         template=ButtonsTemplate(
#             thumbnail_image_url=None,
#             title='キーワード クイズ',
#             text='さて，この世界遺産と関連のあるキーワードはなんでしょう？',
#             actions=actions
#         )
#     )
#     return  buttons_template_message


# def get_random_title():
#     S = requests.Session()
#     URL = f"https://ja.wikipedia.org/w/api.php?action=query&list=random&format=json&rnnamespace=0&rnlimit=1"
#     R = S.get(url=URL)
#     DATA = R.json()
#     return DATA['query']['random'][0]['title']


# def get_wikipedia(title):
#     S = requests.Session()
#     URL = "https://ja.wikipedia.org/w/api.php"

#     PARAMS = {
#         "action": "query",
#         "prop": "revisions",
#         "titles":  title,
#         "rvprop": "content",
#         "format": "json"
#     }

#     # get関数によって情報を取得
#     R = S.get(url=URL, params=PARAMS)
#     DATA = R.json()
#     # jsonから必要なデータの抽出
#     CONTENT = DATA['query']['pages']
#     return CONTENT



# def get_description(title):
#     S = requests.Session()
#     URL = "https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1"
#     PARAMS = {
#         "titles": title
#     }
#     R = S.get(url=URL, params=PARAMS)
#     DATA = R.json()
#     try:
#         pageid = list(DATA['query']['pages'].keys())[0]
#         return DATA['query']['pages'][str(pageid)]['extract']
#     except:
#         return None


# def get_geolocation(mw):
#     geo = re.search(r'\|geo.*?\{\{(?P<geo>.*?)}}', mw)
#     if geo is not None:
#         return geo.group("geo")





# def get_image_url(title):
#     S = requests.Session()
#     URL = f'https://ja.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}'
#     R = S.get(url=URL)
#     DATA = R.json()
#     try:
#         return DATA["thumbnail"]["source"]
#     except:
#         app.logger.warning("no image url")
#         return "https://example.com"


# def delete_braket(mw):
#     mw = re.sub(r'[（(].*?[）)]', '', mw)
#     return mw


# def delete_target_word(mw, target):
#     # 最初に空白を取り除く
#     mw = mw.replace(' ', '')
#     mw = mw.replace('　', '')
#     return mw.replace(target, '<MASK>')

