import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# رابط صورة افتراضية للمارد (يمكنك تغييرها برابط صورة تعجبك)
GENIE_IMAGE_URL = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000&auto=format&fit=crop"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # الأزرار التفاعلية للعبة المارد
    keyboard = [
        [
            InlineKeyboardButton("🧞‍♂️ ابدأ اللعبة (تخمين شخصية)", callback_data="start_game")
        ],
        [
            InlineKeyboardButton("❓ كيف تطرح الأسئلة؟", callback_data="help_game"),
            InlineKeyboardButton("🏆 قائمة الأبطال", callback_data="top_players")
        ],
        [
            InlineKeyboardButton("👑 المطور", url="https://www.facebook.com/profile.php?id=61594929560699")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    caption = (
        "🧞‍♂️ *مرحباً بك في عالم المارد السحري!* 🔮\n\n"
        "هل تستطيع تحدي المارد؟ فكر في شخصية (حقيقية أو خيالية)، وسأقوم بتخمينها من خلال طرح عدة أسئلة عليك.\n\n"
        "✨ اضغط على زر **(ابدأ اللعبة)** بالأسفل لنبدأ المغامرة!"
    )
    
    # إذا تم إرسال الأمر عبر رسالة عادية أو ضغط زر
    if update.message:
        await update.message.reply_photo(
            photo=GENIE_IMAGE_URL,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif update.callback
