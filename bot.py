import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# صور تعبيرية للمارد لكل حالة لضمان ظهور الصور دائماً
GENIE_START_IMG = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000&auto=format&fit=crop"
GENIE_THINKING_IMG = "https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=1000&auto=format&fit=crop"
GENIE_WIN_IMG = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000&auto=format&fit=crop"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['path'] = []
    
    keyboard = [
        [InlineKeyboardButton("🧞‍♂️ ابدأ تحدي المارد", callback_data="ans_start")],
        [InlineKeyboardButton("👑 المطور", url="https://www.facebook.com/profile.php?id=61594929560699")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption = "🧞‍♂️ *مرحباً بك في لعبة المارد السحري الأصلية!* 🔮\n\nفكر في شخصية (أنمي، أسطورية، أو مشهورة)، وسأقوم بتخمينها بدقة من خلال ذكائي الخارق.\n\n✨ اضغط على زر البداية لننطلق!"
    
    if update.message:
        await update.message.reply_photo(photo=GENIE_START_IMG, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.reply_photo(photo=GENIE_START_IMG, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "restart":
        await start(update, context)
        return

    path = context.user_data.get('path', [])
    if data != "ans_start":
        path.append(data)
    context.user_data['path'] = path

    ans_keyboard = [
        [InlineKeyboardButton("✅ نعم", callback_data="yes"), InlineKeyboardButton("❌ لا", callback_data="no")],
        [InlineKeyboardButton("🔄 ربما / لا أعلم", callback_data="maybe")],
        [InlineKeyboardButton("🔄 إعادة اللعبة", callback_data="restart")]
    ]

    # محرك تخمين ذكي بناءً على إجابات المستخدم المتسلسلة
    if len(path) == 0:
        await query.message.delete()
        await query.message.reply_photo(
            photo=GENIE_THINKING_IMG,
            caption="🔮 *السؤال الأول:* هل الشخصية التي تفكر فيها شخصية حقيقية وليست خيالية (أو من واقعنا)؟",
            reply_markup=InlineKeyboardMarkup(ans_keyboard),
            parse_mode="Markdown"
        )
    elif len(path) == 1:
        await query.message.delete()
        await query.message.reply_photo(
            photo=GENIE_THINKING_IMG,
            caption="🔮 *السؤال الثاني:* هل هذه الشخصية مشهورة في عالم الأنمي أو مسلسلات الكرتون؟",
            reply_markup=InlineKeyboardMarkup(ans_keyboard),
            parse_mode="Markdown"
        )
    elif len(path) == 2:
        await query.message.delete()
        await query.message.reply_photo(
            photo=GENIE_THINKING_IMG,
            caption="🔮 *السؤال الثالث:* هل الشخصية تمتلك قوى خارقة أو قدرات غير معتادة؟",
            reply_markup=InlineKeyboardMarkup(ans_keyboard),
            parse_mode="Markdown"
        )
    else:
        # مرحلة التخمين الذكي والنتيجة النهائية
        guess = "شخصية أسطورية أو بطل أنمي شهير!"
        if path[0] == "yes":
            guess = "شخصية تاريخية أو مشهورة عالمياً!"
        elif path[1] == "yes":
            guess = "بطل أنمي خارق ومميز!"

        win_keyboard = [
            [InlineKeyboardButton("🎉 نعم! لقد خمنتها صحيحة!", callback_data="restart")],
            [InlineKeyboardButton("❌ خطأ، حاول مجدداً", callback_data="restart")]
        ]
        
        await query.message.delete()
        await query.message.reply_photo(
            photo=GENIE_WIN_IMG,
            caption=f"✨ *لقد تركزت طاقاتي ووصلت للإجابة!* 🧞‍♂️\n\nأعتقد أن الشخصية التي تفكر فيها هي:\n👉 **{guess}**\n\nهل كنت دقيقاً في تخميني؟",
            reply_markup=InlineKeyboardMarkup(win_keyboard),
            parse_mode="Markdown"
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("Genie Game Bot is running...")
    application.run_polling()
