import os
import telebot
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

Thread(target=run, daemon=True).start()

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8986124658:AAEHNiey_GDxU-Z3CQKg6_"
QR_CODE_URL = "https://i.ibb.co/68032549/image"

if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    pricing_text = (
        "✨ **Welcome! Hamare Services & Rates:**\n"
        "🎥 **2 Min Video** - ₹150\n"
    )
