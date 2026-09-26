import os
import threading
from flask import Flask
import telebot

# --- 1. Flask Server (Keep-Alive ke liye taaki bot so na jaye) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# --- 2. Telegram Bot Setup ---
BOT_TOKEN = "8838547784:AAGLp823nS_JpgVjbSHnOBmQUuFQ_mmMSKc"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Bot is online and running 24/7 🚀")

# Agar aapko aur bhi commands ya UPI payment wale messages lagane hain, toh unhe yahan niche add kar sakte hain
@bot.message_handler(func=lambda message: True)
def default_response(message):
    bot.reply_to(message, "Bot is active! Type /start to continue.")


# --- 3. Start Both Server and Bot ---
if __name__ == "__main__":
    # Pehle background me Flask server chalega
    keep_alive()
    
    print("Bot and Flask server are starting...")
    # Phir Telegram bot polling start hogi
    bot.infinity_polling()
