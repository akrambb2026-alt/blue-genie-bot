import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

QUESTIONS = {
    "q1": {
        "text": "🧞‍♂️ **[المارد الأزرق - السؤال الأول]**\n\nهل الشخصية التي تفكر بها حقيقية (شخصية واقعية) أم خيالية؟",
        "answers": {
            "yes": "q2_real",
            "no": "q2_anime",
            "probably": "q2_real",
            "probably_not": "q2_anime",
            "idk": "q2_real"
        }
    },
    "q2_real": {
        "text": "🧞‍♂️ **[المارد الأزرق - قسم الواقعيات]**\n\nهل هذه الشخصية مشهورة في مجال الرياضة وكرة القدم؟",
        "answers": {
            "yes": "res_messi",
            "no": "res_elon",
            "probably": "res_messi",
            "probably_not": "res_elon",
            "idk": "res_messi"
        }
    },
    "q2_anime": {
        "text": "🧞‍♂️ **[المارد الأزرق - قسم الخيال]**\n\nهل الشخصية من عالم الأنمي أو الكرتون الشهير؟",
        "answers": {
            "yes": "res_naruto",
            "no": "res_spiderman",
            "probably": "res_naruto",
            "probably_not": "res_spiderman",
            "idk": "res_naruto"
        }
    }
}

RESULTS = {
    "res_messi": "⚽ **لقد عرفتها! الشخصية هي:**\n\nليونيل ميسي (Lionel Messi) 🇦🇷🐐\n\nهل حزرت بشكل صحيح؟ 🧞‍♂️",
    "res_elon": "🚀 **لقد عرفتها! الشخصية هي:**\n\nإيلون ماسك (Elon Musk) 🇺🇸💡\n\nهل حزرت بشكل صحيح؟ 🧞‍♂️",
    "res_naruto": "🍥 **لقد عرفتها! الشخصية هي:**\n\nناروتو أوزوماكي (Naruto Uzumaki) 🍜\n\nهل حزرت بشكل صحيح؟ 🧞‍♂️",
    "res_spiderman": "🕷️ **لقد عرفتها! الشخصية هي:**\n\nسبايدرمان (Spider-Man) 🏙️\n\nهل حزرت بشكل صحيح؟ 🧞‍♂️"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("ابدأ اللعبة 🧞‍♂️", callback_data="q1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "أهلاً بك في لعبة **المارد الأزرق (Akinator)** 🧞‍♂️✨\n\nفكر في شخصية في سرك، وسأطرح عليك أسئلة لأعرفها!"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

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
            [InlineKeyboardButton("🤔 ربما", callback_data=q_data["answers"]["probably"]),
             InlineKeyboardButton("👎 غالباً لا", callback_data=q_data["answers"]["probably_not"])],
            [InlineKeyboardButton("🤷‍♂️ لا أعلم", callback_data=q_data["answers"]["idk"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(q_data["text"], reply_markup=reply_markup, parse_mode="Markdown")

    elif data in RESULTS:
        result_text = RESULTS[data]
        keyboard = [[InlineKeyboardButton("إعادة اللعب 🔄", callback_data="restart")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(result_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("🧞‍♂️ المارد يعمل الآن بنجاح تام وبدون أخطاء اتصالات...")
    app.run_polling()

if __name__ == "__main__":
    main()
