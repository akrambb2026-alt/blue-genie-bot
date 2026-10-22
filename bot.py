import os
import akinator
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GENIE_IMAGE_URL = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000&auto=format&fit=crop"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧞‍♂️ ابدأ تحدي المارد الحقيقي", callback_data="start_aki")],
        [InlineKeyboardButton("👑 المطور", url="https://www.facebook.com/profile.php?id=61594929560699")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption = "🧞‍♂️ *مرحباً بك في لعبة المارد السحري الأصلية!* 🔮\n\nفكر في أي شخصية في العالم، وسأقوم بتخمين اسمها بدقة عبر محرك Akinator!\n\n✨ اضغط ابدأ لننطلق!"
    
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

    try:
        if data == "start_aki":
            aki = akinator.Akinator()
            q = aki.start_game(language='ar')
            context.user_data['aki'] = aki
            
            keyboard = [
                [InlineKeyboardButton("✅ نعم", callback_data="ans_0"), InlineKeyboardButton("❌ لا", callback_data="ans_1")],
                [InlineKeyboardButton("⚠️ لا أعلم", callback_data="ans_2"), InlineKeyboardButton("🔄 ربما", callback_data="ans_3")],
                [InlineKeyboardButton("🔙 ربما لا", callback_data="ans_4")]
            ]
            await query.edit_message_caption(
                caption=f"🔮 *السؤال:* {q}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            
        elif data.startswith("ans_"):
            answer_num = int(data.split("_")[1])
            aki = context.user_data.get('aki')
            
            if not aki:
                aki = akinator.Akinator()
                aki.start_game(language='ar')
                context.user_data['aki'] = aki
                
            q = aki.answer(answer_num)
            
            if aki.progression >= 80 or aki.step >= 15:
                aki.win()
                name = aki.first_guess.get('name', 'شخصية غير معروفة')
                desc = aki.first_guess.get('description', '')
                photo_url = aki.first_guess.get('absolute_picture_path', GENIE_IMAGE_URL)
                
                win_keyboard = [[InlineKeyboardButton("🔄 لعب مرة أخرى", callback_data="start_aki")]]
                
                await query.message.delete()
                await query.message.reply_photo(
                    photo=photo_url,
                    caption=f"✨ *لقد خمنت شخصيتك!* 🧞‍♂️\n\nالشخصية هي: **{name}**\n📝 ({desc})\n\nهل كنت دقيقاً معك؟",
                    reply_markup=InlineKeyboardMarkup(win_keyboard),
                    parse_mode="Markdown"
                )
            else:
                keyboard = [
                    [InlineKeyboardButton("✅ نعم", callback_data="ans_0"), InlineKeyboardButton("❌ لا", callback_data="ans_1")],
                    [InlineKeyboardButton("⚠️ لا أعلم", callback_data="ans_2"), InlineKeyboardButton("🔄 ربما", callback_data="ans_3")],
                    [InlineKeyboardButton("🔙 ربما لا", callback_data="ans_4")]
                ]
                await query.edit_message_caption(
                    caption=f"🔮 *السؤال:* {q}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown"
                )
    except Exception as e:
        error_keyboard = [[InlineKeyboardButton("🔄 إعادة المحاولة", callback_data="start_aki")]]
        await query.edit_message_caption(
            caption="⚠️ حدث ضغط على السيرفر أو انقطع الاتصال مؤقتاً. اضغط لإعادة المحاولة:",
            reply_markup=InlineKeyboardMarkup(error_keyboard)
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("Genie Akinator Bot is running...")
    application.run_polling()
