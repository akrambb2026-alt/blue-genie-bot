import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

GENIE_IMAGE_URL = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000&auto=format&fit=crop"
QUESTION_IMAGE_2 = "https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=1000&auto=format&fit=crop"
QUESTION_IMAGE_3 = "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?q=80&w=1000&auto=format&fit=crop"
WIN_IMAGE = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000&auto=format&fit=crop"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧞‍♂️ ابدأ اللعبة (تخمين شخصية)", callback_data="q1")],
        [InlineKeyboardButton("❓ كيف تطرح الأسئلة؟", callback_data="help_game"), InlineKeyboardButton("🏆 قائمة الأبطال", callback_data="top_players")],
        [InlineKeyboardButton("👑 المطور", url="https://www.facebook.com/profile.php?id=61594929560699")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption = "🧞‍♂️ *مرحباً بك في عالم المارد السحري!* 🔮\n\nفكر في شخصية وسأقوم بتخمينها عبر أسئلة ذكية.\n\n✨ اضغط **(ابدأ اللعبة)** لنبدأ!"
    
    if update.message:
        await update.message.reply_photo(photo=GENIE_IMAGE_URL, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.reply_photo(photo=GENIE_IMAGE_URL, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    standard_buttons = [
        [InlineKeyboardButton("✅ نعم", callback_data="yes_next"), InlineKeyboardButton("❌ لا", callback_data="no_next")],
        [InlineKeyboardButton("🔙 العودة للقائمة", callback_data="back_home")]
    ]
    
    if data in ["q1", "yes_next", "no_next"]:
        reply_markup = InlineKeyboardMarkup(standard_buttons)
        await query.edit_message_caption(
            caption="🔮 *السؤال الأول:* هل الشخصية التي تفكر فيها حقيقية وليست خيالية؟",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif data == "help_game":
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]
        await query.edit_message_caption(caption="ℹ️ *طريقة اللعب:*\n1. فكر في شخصية.\n2. أجب بصدق.\n3. دع المارد يخمنها!", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    elif data == "top_players":
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]
        await query.edit_message_caption(caption="🏆 *قائمة الأبطال:*\nلم يتم تسجيل تحديات بعد.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    elif data == "back_home":
        keyboard = [
            [InlineKeyboardButton("🧞‍♂️ ابدأ اللعبة (تخمين شخصية)", callback_data="q1")],
            [InlineKeyboardButton("❓ كيف تطرح الأسئلة؟", callback_data="help_game"), InlineKeyboardButton("🏆 قائمة الأبطال", callback_data="top_players")],
            [InlineKeyboardButton("👑 المطور", url="https://www.facebook.com/profile.php?id=61594929560699")]
        ]
        await query.edit_message_caption(caption="🧞‍♂️ *مرحباً بك من جديد!* 🔮\n\nاختر أحد الخيارات:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("Genie Game Bot is running...")
    application.run_polling()
