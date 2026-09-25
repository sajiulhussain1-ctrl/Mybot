import os
import telebot
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

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
BOT_TOKEN = "8838547784:AAFYDcGPKNTaxkNdWWZ-lV-K0NhbbNGz56Q"
QR_CODE_URL = "https://i.ibb.co/C0315k2/qr.png"

# Aapke 5 Promo Photos ke Direct Links:
START_PHOTOS = [
    "https://i.ibb.co/LBWL674/image.jpg",
    "https://i.ibb.co/V0ht4STK/image.jpg",
    "https://i.ibb.co/HfH47ZT3/image.jpg",
    "https://i.ibb.co/7dspqTHk/image.jpg",
    "https://i.ibb.co/hxkBBHWW/image.jpg"
]

if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    # 1. Start dabate hi pehle 5 Promo Photos aayengi
    try:
        media_group = [InputMediaPhoto(url) for url in START_PHOTOS]
        bot.send_media_group(message.chat.id, media_group)
    except Exception as e:
        print("Media group send error:", e)

    # 2. Photos ke sath Rates & Pay Button aayega
    pricing_text = (
        "<b>✨ Welcome to Taniya Exclusive Service ✨</b>\n\n"
        "🔥 <b>Available Rates & Packages:</b>\n\n"
        "📹 <b>2 Min Open Video:</b> ₹150\n"
        "📹 <b>5 Min Open Video:</b> ₹300\n"
        "👩‍🦰 <b>10 Min Video (With Face):</b> ₹500\n"
        "📞 <b>WhatsApp Video Call (VC):</b> ₹700\n\n"
        "👇 <b>Payment karne ke liye niche 'Pay Now / Scan QR' button par click karein!</b>"
    )
    
    markup = InlineKeyboardMarkup()
    btn_pay = InlineKeyboardButton("💳 Pay Now / Scan QR", callback_data="pay_qr")
    markup.add(btn_pay)
    
    bot.send_message(message.chat.id, pricing_text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "pay_qr")
def send_qr_code(call):
    caption_text = (
        "📌 <b>Payment Details & Instructions:</b>\n\n"
        "1️⃣ <b>Option 1:</b> Upar diye gaye QR Code ko scan karke payment karein.\n"
        "2️⃣ <b>Option 2:</b> Direct UPI ID par pay karein:\n"
        "   • <b>UPI ID:</b> <code>mitali55@ptaxis</code>\n\n"
        "3️⃣ Payment complete hone ke baad screenshot is chat me bhejein.\n"
        "4️⃣ Screenshot milne ke baad aapki service instantly start kar di jayegi! ✅"
    )
    
    try:
        bot.send_photo(call.message.chat.id, photo=QR_CODE_URL, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        fallback_text = (
            "📌 <b>Payment Details & Instructions:</b>\n\n"
            "👉 <b>UPI ID:</b> <code>mitali55@ptaxis</code>\n\n"
            "1️⃣ Upar di gayi UPI ID par payment karein.\n"
            "2️⃣ Payment complete hone ke baad screenshot is chat me bhejein.\n"
            "3️⃣ Screenshot milne ke baad aapki service instantly start kar di jayegi! ✅"
        )
        bot.send_message(call.message.chat.id, fallback_text, parse_mode="HTML")
        
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_name = f"screenshots/{message.from_user.id}_{message.message_id}.jpg"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "✅ <b>Payment Screenshot Received!</b>\nHum aapka payment verify kar rahe hain. Aapki service instant receive ho jayegi.", parse_mode="HTML")

# Continuous Polling Loop
bot.infinity_polling(timeout=10, long_polling_timeout=5)
