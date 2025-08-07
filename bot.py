import sys
print("Python version:", sys.version)

import logging
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Підключення до Google Таблиці
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Отримуємо таблицю
spreadsheet_url = os.getenv("SHEET_URL")
spreadsheet = client.open_by_url(spreadsheet_url)
worksheet = spreadsheet.sheet1

# Логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот танцювальної студії")

# Команда /check
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    values = worksheet.get_all_values()

    header = values[0]
    id_index = header.index("Telegram ID") if "Telegram ID" in header else None

    if id_index is None:
        await update.message.reply_text("У таблиці не знайдено колонку 'Telegram ID'.")
        return

    for row in values[1:]:
        if len(row) > id_index and row[id_index] == user_id:
            name = row[0]
            visit_count = row[2]
            days_left = row[3]
            await update.message.reply_text(
                f"Ім'я: {name}\nВідвідувань: {visit_count}\nДнів до завершення: {days_left}"
            )
            return

    await update.message.reply_text("Ваш ID не знайдено в таблиці.")

# Запуск бота
if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    app.bot.set_my_commands([
        BotCommand("check", "Перевірити своє відвідування")
    ])

    print("Бот запущено...")
    app.run_polling()

