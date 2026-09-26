import os
import threading
from flask import Flask
import telebot

# --- 1. Flask Server (Keep-Alive ke liye) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    # Render free tier ke liye port 8080 best hai
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# --- 2. Telegram Bot Setup ---
# Yahan apna Telegram Bot Token daalein
BOT_TOKEN = "APNA_BOT_TOKEN_YAHAN_DAALEIN"
bot = telebot.TeleBot(BOT_TOKEN)

# Aapke bot ki commands / messages yahan aayengi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Bot is online and working fine 🚀")

# Agar aapke paas aur bhi message handlers hain, toh unhe aap yahan niche likh sakte hain:
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


# --- 3. Bot aur Server ko Ek Sath Start Karna ---
if __name__ == "__main__":
    # Pehle background me Flask server chalega
    keep_alive()
    
    # Phir Telegram bot polling start hogi
    print("Bot is starting...")
    bot.infinity_polling()
