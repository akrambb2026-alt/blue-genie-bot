import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GENIE_IMAGE_URL = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000&auto=format&fit=crop"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تصفير مرحلة اللعبة عند البداية
    context.user_data['game_step'] = 0
    
    keyboard = [
        [InlineKeyboardButton("🧞‍♂️ ابدأ اللعبة (تخمين شخصية)", callback_data="next_question")],
        [InlineKeyboardButton("❓ كيف تطرح الأسئلة؟", callback_data="help_game"), InlineKeyboardButton("🏆 قائمة الأبطال", callback_data="top_players")],
        [InlineKeyboardButton("👑 المطور", url="https://www.facebook.com/profile.php?id=61594929560699")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption = "🧞‍♂️ *مرحباً بك في عالم المارد السحري!* 🔮\n\nفكر في شخصية وسأقوم بتخمينها عبر أسئلة ذكية ومتسلسلة.\n\n✨ اضغط **(ابدأ اللعبة)** لنبدأ التحدي!"
    
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
    
    if data == "help_game":
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]
        await query.edit_message_caption(caption="ℹ️ *طريقة اللعب:*\n1. فكر في شخصية.\n2. أجب عن أسئلة المارد بصدق.\n3. سيقوم المارد بتخمين الشخصية بدقة!", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return
    elif data == "top_players":
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="back_home")]]
        await query.edit_message_caption(caption="🏆 *قائمة الأبطال:*\nلم يتم تسجيل تحديات بعد، كن الأول!", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return
    elif data == "back_home":
        await start(update, context)
        return

    # إدارة خطوات اللعبة والأسئلة المتسلسلة
    step = context.user_data.get('game_step', 0)
    
    ans_keyboard = [
        [InlineKeyboardButton("✅ نعم", callback_data="next_question"), InlineKeyboardButton("❌ لا", callback_data="next_question")],
        [InlineKeyboardButton("⚠️ لا أعلم", callback_data="next_question"), InlineKeyboardButton("🔄 ربما", callback_data="next_question")],
        [InlineKeyboardButton("🔙 انسحاب", callback_data="back_home")]
    ]

    if step == 0:
        context.user_data['game_step'] = 1
        await query.edit_message_caption(
            caption="🔮 *السؤال الأول:* هل الشخصية التي تفكر فيها حقيقية وليست خيالية؟",
            reply_markup=InlineKeyboardMarkup(ans_keyboard),
            parse_mode="Markdown"
        )
    elif step == 1:
        context.user_data['game_step'] = 2
        await query.edit_message_caption(
            caption="🔮 *السؤال الثاني:* هل الشخصية مشهورة في عالم الأنمي أو الأفلام؟",
            reply_markup=InlineKeyboardMarkup(ans_keyboard),
            parse_mode="Markdown"
        )
    elif step == 2:
        context.user_data['game_step'] = 3
        await query.edit_message_caption(
            caption="🔮 *السؤال الثالث:* هل الشخصية ذكر أم أنثى؟",
            reply_markup=InlineKeyboardMarkup(ans_keyboard),
            parse_mode="Markdown"
        )
    else:
        # مرحلة التخمين النهائي بعد انتهاء الأسئلة
        final_keyboard = [
            [InlineKeyboardButton("🎉 نعم، هذه هي الشخصية!", callback_data="back_home")],
            [InlineKeyboardButton("❌ لست هي، حاول مجدداً", callback_data="back_home")]
        ]
        context.user_data['game_step'] = 0
        await query.edit_message_caption(
            caption="✨ *لقد توصلت للإجابة!* 🧞‍♂️\n\nأعتقد أن الشخصية التي تفكر فيها هي: **بطل اسطوري**!\n\nهل كنت أخمّن بشكل صحيح؟",
            reply_markup=InlineKeyboardMarkup(final_keyboard),
            parse_mode="Markdown"
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("Genie Game Bot is running...")
    application.run_polling()
