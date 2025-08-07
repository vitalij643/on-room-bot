import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

TOKEN = os.getenv("BOT_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")

bot = telebot.TeleBot(TOKEN)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привіт! Я бот для перевірки відвідуваності. Напиши /checkin щоб відмітити присутність.")

@bot.message_handler(commands=['checkin'])
def checkin(message):
    user = message.from_user
    name = f"{user.first_name} {user.last_name or ''}".strip()
    telegram_id = user.id

    sheet.append_row([name, str(telegram_id), "✅", message.date])
    bot.reply_to(message, "Твій прихід успішно зафіксовано!")

bot.infinity_polling()