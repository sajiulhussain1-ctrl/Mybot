import os
import telebot
from flask import Flask
from threading import Thread

# Flask App setup for Render Keep-Alive Heartbeat
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run, daemon=True).start()

# Bot Setup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8838547784:AAFYDcGPKNTaxkNdWWZ-lV-K0NhbbNGz56Q"
QR_CODE_URL = "https://i.ibb.co/68032549/image.png"

if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    pricing_text = (
        "<b>✨ Welcome to Taniya Exclusive Official Bot! ✨</b>\n\n"
        "🔥 <b>Exclusive VIP Membership Plans</b> 🔥\n\n"
        "🔹 <b>1 Month VIP:</b> ₹199\n"
        "🔹 <b>3 Months VIP:</b> ₹399\n"
        "🔹 <b>Lifetime VIP:</b> ₹699\n\n"
        "👇 <b>Payment karne ke liye niche 'Pay Now / Scan QR' button par click karein!</b>"
    )
    
    markup = InlineKeyboardMarkup()
    btn_pay = InlineKeyboardButton("💳 Pay Now / Scan QR", callback_data="pay_qr")
    markup.add(btn_pay)
    
    bot.reply_to(message, pricing_text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "pay_qr")
def send_qr_code(call):
    caption_text = (
        "📌 <b>Payment Instruction:</b>\n\n"
        "1️⃣ Upar diye gaye QR Code ko scan karke payment karein.\n"
        "2️⃣ Payment hone ke baad screenshot yahan chat me bhejein.\n"
        "3️⃣ Screenshot milne ke baad aapka VIP Access instantly activate kar diya jayega!"
    )
    bot.send_photo(call.message.chat.id, photo=QR_CODE_URL, caption=caption_text, parse_mode="HTML")
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_name = f"screenshots/{message.from_user.id}_{message.message_id}.jpg"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "✅ <b>Payment Screenshot Received!</b>\nHum aapka payment verify kar rahe hain. Jaldi hi VIP link bhej diya jayega.", parse_mode="HTML")

# Continuous Polling Loop
bot.infinity_polling(timeout=10, long_polling_timeout=5)
