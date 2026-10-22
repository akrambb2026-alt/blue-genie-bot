import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

# صور المارد والشخصيات
GENIE_IMAGE = "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=600" # صورة تعبيرية للمارد

QUESTIONS = {
    "q1": {
        "text": "🧞‍♂️ **المارد الأزرق يفكر...**\n\nهل الشخصية حقيقية أم خيالية؟",
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600",
        "answers": {
            "yes": "q2_real",      # حقيقية
            "no": "q2_anime",      # خيالية
            "probably": "q2_real", # ربما
            "probably_not": "q2_anime",
            "idk": "q2_real"
        }
    },
    "q2_real": {
        "text": "🧞‍♂️ **ممم...**\n\nهل الشخصية مشهورة في مجال الرياضة؟",
        "image": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=600",
        "answers": {
            "yes": "q3_football",
            "no": "q3_tech",
            "probably": "q3_football",
            "probably_not": "q3_tech",
            "idk": "q3_football"
        }
    },
    "q3_football": {
        "text": "🧞‍♂️ **أها!**\n\nهل لعب هذه الشخصية لنادي برشلونة أو يفوز بالكرات الذهبية بكثرة؟",
        "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=600",
        "answers": {
            "yes": "res_messi",
            "no": "res_ronaldo",
            "probably": "res_messi",
            "probably_not": "res_ronaldo",
            "idk": "res_messi"
        }
    },
    "q3_tech": {
        "text": "🧞‍♂️ **يدور في ذهني شيء...**\n\nهل تمتك هذه الشخصية شركات فضاء أو سيارات كهربائية (مثل Tesla)؟",
        "image": "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=600",
        "answers": {
            "yes": "res_elon",
            "no": "res_yt",
            "probably": "res_elon",
            "probably_not": "res_yt",
            "idk": "res_elon"
        }
    },
    "q2_anime": {
        "text": "🧞‍♂️ **شخصية خيالية!**\n\nهل الشخصية من عالم الأنمي والمانغا؟",
        "image": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600",
        "answers": {
            "yes": "q3_anime_hair",
            "no": "res_spiderman",
            "probably": "q3_anime_hair",
            "probably_not": "res_spiderman",
            "idk": "q3_anime_hair"
        }
    },
    "q3_anime_hair": {
        "text": "🧞‍♂️ **رائع!**\n\nهل الشخصية تحلم بأن تصبح هوكاجي ولديها شعر أصفر؟",
        "image": "https://images.unsplash.com/photo-1563089145-599997674d42?w=600",
        "answers": {
            "yes": "res_naruto",
            "no": "res_luffy",
            "probably": "res_naruto",
            "probably_not": "res_luffy",
            "idk": "res_naruto"
        }
    }
}

RESULTS = {
    "res_messi": {
        "title": "⚽ **ليونيل ميسي (Lionel Messi)**",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Lionel_Messi_20180626.jpg/440px-Lionel_Messi_20180626.jpg"
    },
    "res_ronaldo": {
        "title": "🇵🇹 **كريستيانو رونالدو (Cristiano Ronaldo)**",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cristiano_Ronaldo_2018.jpg/440px-Cristiano_Ronaldo_2018.jpg"
    },
    "res_elon": {
        "title": "🚀 **إيلون ماسك (Elon Musk)**",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg/440px-Elon_Musk_Royal_Society_%28crop2%29.jpg"
    },
    "res_naruto": {
        "title": "🍥 **ناروتو أوزوماكي (Naruto Uzumaki)**",
        "img": "https://images.unsplash.com/photo-1563089145-599997674d42?w=600"
    },
    "res_luffy": {
        "title": "🏴‍☠️ **مونكي دي لوفي (Monkey D. Luffy)**",
        "img": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600"
    },
    "res_spiderman": {
        "title": "🕷️ **سبايدرمان (Spider-Man)**",
        "img": "https://images.unsplash.com/photo-1604200213928-ba3cf4fc8436?w=600"
    },
    "res_yt": {
        "title": "🎥 **مستشار أو صانع محتوى مشهور (YouTuber)**",
        "img": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=600"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("ابدأ اللعبة 🧞‍♂️", callback_data="q1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption = "أهلاً بك في لعبة **المارد الأزرق** الاحترافية! 🧞‍♂️✨\n\nفكر في أي شخصية (حقيقية، أنمي، رياضية...) وسأحاول التخمين بأزرار فائقة!"
    
    if update.message:
        await update.message.reply_photo(photo=GENIE_IMAGE, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        query = update.callback_query
        await query.message.reply_photo(photo=GENIE_IMAGE, caption=caption, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "restart":
        await start(update, context)
        return

    if data in QUESTIONS:
        q_data = QUESTIONS[data]
        # أزرار واقعية واحترافية مثل لعبة أكيناتور الأصلية
        keyboard = [
            [InlineKeyboardButton("✅ نعم", callback_data=q_data["answers"]["yes"]),
             InlineKeyboardButton("❌ لا", callback_data=q_data["answers"]["no"])],
            [InlineKeyboardButton("🤔 ربما", callback_data=q_data["answers"]["probably"]),
             InlineKeyboardButton("👎 غالباً لا", callback_data=q_data["answers"]["probably_not"])],
            [InlineKeyboardButton("🤷‍♂️ لا أعلم", callback_data=q_data["answers"]["idk"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await query.message.delete()
        except:
            pass
        await query.message.reply_photo(photo=q_data["image"], caption=q_data["text"], reply_markup=reply_markup, parse_mode="Markdown")

    elif data in RESULTS:
        res = RESULTS[data]
        result_text = f"🔮 **وجدتها! الشخصية هي:**\n\n{res['title']}\n\nهل حزرت بشكل صحيح؟ 🧞‍♂️"
        keyboard = [[InlineKeyboardButton("إعادة اللعب 🔄", callback_data="restart")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await query.message.delete()
        except:
            pass
        await query.message.reply_photo(photo=res["img"], caption=result_text, reply_markup=reply_markup, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("🧞‍♂️ البوت يعمل الآن بكامل قوته...")
    app.run_polling()

if __name__ == "__main__":
    main()
