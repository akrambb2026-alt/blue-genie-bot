import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os

# التوكن الخاص بك
TOKEN = "8853392027:AAGa4P7WIwD-LMUmy4kYu4x-UkRMOfQs2mc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('مرحباً بك! أنا المارد السحري، أرسل لي أي صورة لأقوم بمعالجتها بالذكاء الاصطناعي ✨')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('لقد استلمت رسالتك/صورتك، جاري المعالجة...')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.ALL, handle_message))
    
    application.run_polling()
