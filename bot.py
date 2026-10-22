import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

# صورة ثابتة وموحدة للمارد الأزرق طوال فترة طرح الأسئلة (مثل اللعبة الأصلية)
GENIE_THINKING_IMAGE = "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600"

QUESTIONS = {
    "q1": {
        "text": "🧞‍♂️ **السؤال (1):** هل الشخصية التي تفكر بها حقيقية (شخصية واقعية) أم خيالية؟",
        "answers": {
            "yes": "q2_real",
            "no": "q2_anime",
            "probably": "q2_real",
            "probably_not": "q2_anime",
            "idk": "q2_real"
        }
    },
    "q2_real": {
        "text": "🧞‍♂️ **السؤال (2):** هل هذه الشخصية مشهورة في مجال الرياضة وكرة القدم؟",
        "answers": {
            "yes": "res_messi",
            "no": "res_elon",
            "probably": "res_messi",
            "probably_not": "res_elon",
            "idk": "res_messi"
        }
    },
    "q2_anime": {
        "text": "🧞‍♂️ **السؤال (2):** هل الشخصية من عالم الأنمي أو الكرتون الشهير؟",
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
    "res_messi": {
        "title": "⚽ **ليونيل ميسي (Lionel Messi)**",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Lionel_Messi_20180626.jpg/440px-Lionel_Messi_20180626.jpg"
    },
    "res_elon": {
        "title": "🚀 **إيلون ماسك (Elon Musk)**",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg/440px-Elon_Musk_Royal_Society_%28crop2%29.jpg"
    },
    "res_naruto": {
        "title": "🍥 **ناروتو أوزوماكي (Naruto Uzumaki)**",
        "img": "https://images.unsplash.com/photo-1563089145-599997674d42?w=600"
    },
    "res_spiderman": {
        "title": "🕷️ **سبايدرمان (Spider-Man)**",
        "img": "https://images.unsplash.com/photo-1604200213928-ba3cf4fc8436?w=600"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("ابدأ اللعبة 🧞‍♂️", callback_data="q1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption = "أهلاً بك في لعبة **المارد الأزرق (Akinator)** الحقيقية! 🧞‍♂️✨\n\nفكر في شخصية وسأحاول تخمينها بأسئلة ذكية."
    
    if update.message:
        await update.message.reply_photo(photo=GENIE_THINKING_IMAGE, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.message.reply_photo(photo=GENIE_THINKING_IMAGE, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")

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
        # إرسال نفس صورة المارد أثناء التفكير مع السؤال الجديد لتبقى اللعبة واقعية تماماً
        await query.message.reply_photo(photo=GENIE_THINKING_IMAGE, caption=q_data["text"], reply_markup=reply_markup, parse_mode="Markdown")

    elif data in RESULTS:
        res = RESULTS[data]
        result_text = f"🔮 **المارد يقول: لقد وجدت الشخصية!**\n\nالشخصية هي: {res['title']}\n\nهل حزرت بشكل صحيح؟ 🧞‍♂️"
        keyboard = [[InlineKeyboardButton("إعادة اللعب 🔄", callback_data="restart")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # إرسال صورة الشخصية فقط عند التخمين النهائي
        await query.message.reply_photo(photo=res["img"], caption=result_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("🧞‍♂️ المارد يعمل الآن بطريقة احترافية تشبه اللعبة الحقيقية...")
    app.run_polling()

if __name__ == "__main__":
    main()
