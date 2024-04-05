from flask import Flask, request, abort
import os
import json
import requests

app = Flask(__name__)

# 從環境變數中讀取 Line Bot 的 Channel Access Token 和 Channel Secret
LINE_ACCESS_TOKEN = None
LINE_CHANNEL_SECRET = None

# 從文件中讀取 Line Bot 的 Channel Access Token 和 Channel Secret
with open("linebot_config.json", "r") as f:
  config = json.load(f)
  LINE_ACCESS_TOKEN = config.get("LINE_ACCESS_TOKEN")
  LINE_CHANNEL_SECRET = config.get("LINE_CHANNEL_SECRET")

# 確認環境變數存在
if LINE_ACCESS_TOKEN is None or LINE_CHANNEL_SECRET is None:
  print("請設置 LINE_ACCESS_TOKEN 和 LINE_CHANNEL_SECRET 環境變數")
  exit()

# 初始化 LineBotApi 和 WebhookHandler
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/")
def hello():
  return "Hello World!"


@app.route("/callback", methods=["POST"])
def callback():
  signature = request.headers["X-Line-Signature"]
  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    abort(400)

  return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  text = event.message.text
  reply_text = get_reply(text)
  line_bot_api.reply_message(event.reply_token,
                             TextSendMessage(text=reply_text))


def get_reply(text):
  # 根據收到的訊息 text 返回相對應的回覆
  # 這裡可以自行定義回覆的邏輯
  if "晚餐已訂好" in text:
    return "好，出門記得要把籃子放出去"


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)

