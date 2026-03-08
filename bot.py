import os
import requests
from telegram.ext import Updater, MessageHandler, Filters

BOT_TOKEN = os.environ["BOT_TOKEN"]
GEMINI_KEY = os.environ["GEMINI_KEY"]

def chat(update, context):
    user_text = update.message.text

    prompt = f"""
You are an English teacher.

1. Talk with the user in English.
2. Correct their sentence.
3. Explain the mistake shortly.
4. Teach one new English word.

User sentence:
{user_text}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"

    data = {
        "contents":[{"parts":[{"text":prompt}]}]
    }

    r = requests.post(url, json=data)
    result = r.json()

    try:
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        reply = "AI response error."

    update.message.reply_text(reply)

updater = Updater(BOT_TOKEN, use_context=True)

dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

print("Bot started...")

updater.start_polling()
updater.idle()
