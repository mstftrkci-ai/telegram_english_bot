import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ["AAGDzXfVPuOeeTEQ37ZbHSjVzoKTUQjIHU4"]
GEMINI_KEY = os.environ["AIzaSyAkWAGJh5TdhMLYnEan_6LrZv99899gEVw"]

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    response = requests.post(url, json=data)
    result = response.json()

    reply = result["candidates"][0]["content"]["parts"][0]["text"]

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot çalışıyor...")
app.run_polling()