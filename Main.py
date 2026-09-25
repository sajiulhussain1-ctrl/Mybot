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

# Aapki 5 HD Promo Photos File IDs
START_PHOTOS = [
    "AgACAgUAAxkBAAM9arY0RSMLm_ceAhQLTtkl67RmHVQAAnYRaxvRprBVNfoyGs0zCpYBAAMCAAN4AAM9BA",
    "AgACAgUAAxkBAAM3arYzmwYknDv6zsIiT3c0KD5f844AAnQRaxvRprBVVpvbLoUMSWIBAAMCAAN4AAM9BA",
    "AgACAgUAAxkBAANBarY0T7yDAAGC_OrWBuG13FsfpC-FAAJ3EWsb0aawVSlICQq9dJuJAQADAgADeAADPQQ",
    "AgACAgUAAxkBAANDarY0VUamO1E7Z-fHtJG8mtLXsbcAAngRaxvRprBVrD-Ac9UBf1QBAAMCAAN4AAM9BA",
    "AgACAgUAAxkBAANFarY0V90s50KM8xU4IE8v2efwS1QAAnkRaxvRprBV1HYT58Mm_mABAAMCAAN4AAM9BA"
]

# Aapki HD QR Code File ID
QR_CODE_FILE_ID = "AgACAgUAAxkBAAMnarYysY5FAr2oOsMR1HStQjDRUmsAAm4SaxtCi7BVoAXUk2SWYycBAAMCAAN4AAM9BA"

if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    # 1. Start dabate hi 5 Promo Photos HD me aayengi
    try:
        media_group = [InputMediaPhoto(photo_id) for photo_id in START_PHOTOS]
        bot.send_media_group(message.chat.id, media_group)
    except Exception as e:
        print("Media group send error:", e)

    # 2. Rates aur Pay Button
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
        # HD QR Code Photo ke saath UPI ID caption me aayegi
        bot.send_photo(call.message.chat.id, photo=QR_CODE_FILE_ID, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        print("Photo send error:", e)
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

bot.infinity_polling(timeout=10, long_polling_timeout=5)
