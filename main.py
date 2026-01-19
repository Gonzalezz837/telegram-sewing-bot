import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
OWNER_CHAT_ID = int(os.getenv("OWNER_CHAT_ID"))

KEYWORDS = os.getenv("KEYWORDS").lower().split("|")
NEGATIVE = os.getenv("NEGATIVE").lower().split("|")

def is_relevant(text: str) -> bool:
    text = text.lower()

    if any(word in text for word in NEGATIVE):
        return False

    score = 0
    for word in KEYWORDS:
        if word in text:
            score += 1

    return score >= 2  # минимум 2 совпадения

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    if is_relevant(text):
        chat = update.message.chat
        link = f"https://t.me/c/{str(chat.id)[4:]}/{update.message.message_id}" if chat.id < 0 else "Личная группа"

        msg = (
            "🧵 *Найден запрос на пошив*\n\n"
            f"📍 *Группа:* {chat.title}\n\n"
            f"📝 *Текст:*\n{text}\n\n"
            f"🔗 {link}"
        )

        await context.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text=msg,
            parse_mode="Markdown"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

app.run_polling()
