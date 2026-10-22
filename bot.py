import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# رابط صورة افتراضية للمارد السحري
GENIE_IMAGE_URL = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000&auto=format&fit=crop"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    if update.message:
        await update.message.reply_photo(
            photo=GENIE_IMAGE_URL,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.reply_photo(
            photo=GENIE_IMAGE_URL,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "start_game":
        keyboard = [
            [
                InlineKeyboardButton("✅ نعم", callback_data="ans_yes"),
                InlineKeyboardButton("❌ لا", callback_data="ans_no")
            ],
            [
                InlineKeyboardButton("⚠️ لا أعلم", callback_data="ans_idk"),
                InlineKeyboardButton("🔄 ربما جزئياً", callback_data="ans_maybe")
            ],
            [
                InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_home")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(
            caption="🔮 *السؤال الأول:* هل الشخصية التي تفكر فيها حقيقية وليست خيالية؟",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data.startswith("ans_"):
        keyboard = [
            [
                InlineKeyboardButton("✅ نعم", callback_data="ans_yes_2"),
                InlineKeyboardButton("❌ لا", callback_data="ans_no_2")
            ],
            [
                InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_home")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(
            caption="🔮 *السؤال الثاني:* هل الشخصية مشهورة في عالم الأنمي أو الكرتون؟",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data == "help_game":
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="ℹ️ *طريقة اللعب:*\n1. فكر في شخصية في سرك.\n2. أجب عن أسئلة المارد بصدق.\n3. دع المارد يدهشك بتخمين الشخصية بدقة!",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data == "top_players":
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="🏆 *قائمة الأبطال:*\nلم يتم تسجيل أية تحديات حتى الآن، كن أول الفائزين!",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data == "back_home":
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
        await query.edit_message_caption(
            caption="🧞‍♂️ *مرحباً بك من جديد في عالم المارد السحري!* 🔮\n\nاختر أحد الخيارات للبدء:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("Genie Game Bot is running...")
    application.run_polling()
