import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

GENIE_IMAGE_URL = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000&auto=format&fit=crop"
THINK_IMAGE = "https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=1000&auto=format&fit=crop"
WIN_IMAGE = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000&auto=format&fit=crop"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['step'] = 0
    context.user_data['answers'] = []
    
    keyboard = [
        [InlineKeyboardButton("🧞‍♂️ ابدأ تحدي المارد السحري", callback_data="play")],
        [InlineKeyboardButton("👑 المطور", url="https://www.facebook.com/profile.php?id=61594929560699")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption = "🧞‍♂️ *مرحباً بك في لعبة المارد السحري الذكية!* 🔮\n\nفكر في شخصية وسأقوم بتخمينها بدقة من خلال أسئلتي الذكية.\n\n✨ اضغط ابدأ لننطلق!"
    
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

    if data == "restart":
        await start(update, context)
        return

    step = context.user_data.get('step', 0)
    answers = context.user_data.get('answers', [])
    
    if data in ["yes", "no", "maybe"]:
        answers.append(data)
        step += 1
        context.user_data['step'] = step
        context.user_data['answers'] = answers

    ans_keyboard = [
        [InlineKeyboardButton("✅ نعم", callback_data="yes"), InlineKeyboardButton("❌ لا", callback_data="no")],
        [InlineKeyboardButton("⚠️ ربما / لا أعلم", callback_data="maybe")],
        [InlineKeyboardButton("🔄 إعادة اللعبة", callback_data="restart")]
    ]

    try:
        if step == 0:
            context.user_data['step'] = 1
            await query.message.delete()
            await query.message.reply_photo(
                photo=THINK_IMAGE,
                caption="🔮 *السؤال الأول:* هل الشخصية التي تفكر فيها شخصية حقيقية وليست خيالية؟",
                reply_markup=InlineKeyboardMarkup(ans_keyboard),
                parse_mode="Markdown"
            )
        elif step == 1:
            await query.message.delete()
            await query.message.reply_photo(
                photo=THINK_IMAGE,
                caption="🔮 *السؤال الثاني:* هل الشخصية مشهورة في عالم الأنمي أو الكرتون أو الألعاب؟",
                reply_markup=InlineKeyboardMarkup(ans_keyboard),
                parse_mode="Markdown"
            )
        elif step == 2:
            await query.message.delete()
            await query.message.reply_photo(
                photo=THINK_IMAGE,
                caption="🔮 *السؤال الثالث:* هل تمتلك هذه الشخصية قوى خارقة أو قدرات غير معتادة؟",
                reply_markup=InlineKeyboardMarkup(ans_keyboard),
                parse_mode="Markdown"
            )
        elif step == 3:
            await query.message.delete()
            await query.message.reply_photo(
                photo=THINK_IMAGE,
                caption="🔮 *السؤال الرابع:* هل الشخصية ذكر أم ظهرت كبطل رئيسي في قصتها؟",
                reply_markup=InlineKeyboardMarkup(ans_keyboard),
                parse_mode="Markdown"
            )
        else:
            # تحليل الإجابات وتخمين الشخصية بدقة
            ans = context.user_data.get('answers', [])
            guess = "ناروتو أوزوماكي (Naruto)"
            
            if len(ans) > 0 and ans[0] == "yes":
                guess = "ليونيل ميسي أو كريستيانو رونالدو (لاعب مشهور)"
            elif len(ans) > 1 and ans[1] == "yes" and len(ans) > 2 and ans[2] == "yes":
                guess = "غوكو (Goku) أو لوفي (Luffy)"
            elif len(ans) > 0 and ans[0] == "no":
                guess = "شخصية خيالية أو بطل أنمي شهير"

            win_keyboard = [[InlineKeyboardButton("🔄 لعب مرة أخرى", callback_data="restart")]]
            
            await query.message.delete()
            await query.message.reply_photo(
                photo=WIN_IMAGE,
                caption=f"✨ *لقد تركزت طاقاتي ووصلت للإجابة!* 🧞‍♂️\n\nأعتقد أن الشخصية التي تفكر فيها هي:\n👉 **{guess}**\n\nهل كنت دقيقاً في تخميني؟",
                reply_markup=InlineKeyboardMarkup(win_keyboard),
                parse_mode="Markdown"
            )
    except Exception:
        await query.message.reply_text("حدث خطأ بسيط، اضغط /start للبدء من جديد.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("Smart Genie Game Bot is running...")
    application.run_polling()
