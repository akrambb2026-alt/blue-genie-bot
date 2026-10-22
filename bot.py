import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

QUESTIONS = {
    "q1": {
        "text": "🧞‍♂️ المارد الأزرق يفكر...\n\nهل الشخصية حقيقية؟",
        "answers": {"yes": "q2_real", "no": "q2_anime", "idk": "q2_real"}
    },
    "q2_real": {
        "text": "🧞‍♂️ ممم... هل الشخصية لاعب كرة قدم؟",
        "answers": {"yes": "res_messi", "no": "res_tech", "idk": "res_messi"}
    },
    "q2_anime": {
        "text": "🧞‍♂️ أها! هل الشخصية من أنمي محدد ولديه شعر أصفر؟",
        "answers": {"yes": "res_naruto", "no": "res_luffy", "idk": "res_luffy"}
    }
}

RESULTS = {
    "res_messi": "⚽ الشخصية التي تفكر بها هي: **ليونيل ميسي**!",
    "res_tech": "💻 الشخصية التي تفكر بها هي: **إيلون ماسك**!",
    "res_naruto": "🍥 الشخصية التي تفكر بها هي: **ناروتو أوزوماكي**!",
    "res_luffy": "🏴‍☠️ الشخصية التي تفكر بها هي: **مونكي دي لوفي**!"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("ابدأ اللعبة 🧞‍♂️", callback_data="q1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = "أهلاً بك في لعبة المارد الأزرق! 🧞‍♂️✨\n\nفكر في شخصية وسأحاول تخمينها!"
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.message.edit_text(welcome_text, reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "restart":
        await start(update, context)
        return

    if data in QUESTIONS:
        q_data = QUESTIONS[data]
        keyboard = [
            [InlineKeyboardButton("✅ نعم", callback_data=q_data["answers"]["yes"]),
             InlineKeyboardButton("❌ لا", callback_data=q_data["answers"]["no"])],
            [InlineKeyboardButton("🤷‍♂️ لا أعلم", callback_data=q_data["answers"]["idk"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(q_data["text"], reply_markup=reply_markup)
    elif data in RESULTS:
        result_text = f"🔮 **وجدتها!**\n\n{RESULTS[data]}\n\nهل حزرت بشكل صحيح؟"
        keyboard = [[InlineKeyboardButton("إعادة اللعب 🔄", callback_data="restart")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(result_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("🧞‍♂️ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
