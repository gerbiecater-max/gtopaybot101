import os
import logging
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# keep_alive portion
app = Flask("keep_alive")

@app.route("/")
def home():
    return "Bot is running."

def run_web():
    port = int(os.environ.get("PORT", 8080))  # Render sets PORT env var
    # listen on 0.0.0.0 so external checks succeed
    app.run(host="0.0.0.0", port=port)

def start_keep_alive():
    t = Thread(target=run_web, daemon=True)
    t.start()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Store your token in .env file

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This button opens your web mini app (replace URL with your hosted page)
    payment_web_app = WebAppInfo(url="https://gtopay.com.ng")
    login_web_app = WebAppInfo(url="https://gtopay.com.ng/?login")
    download_web_app = WebAppInfo(url="https://sabuss.com/gtopay1?download")
    # Main keyboard with web apps
    keyboard = [
        [KeyboardButton(text="💳 Open GTOPay", web_app=payment_web_app)],
        [KeyboardButton(text="🔐 Login/Sign Up", web_app=login_web_app)],
        [KeyboardButton(text="⬇️ Download GTOPay", web_app=download_web_app)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Inline keyboard for app download
    inline_keyboard = [
        [InlineKeyboardButton(text="📱 Download Android App", url="https://sabuss.com/gtopay1?download")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    
    # Send main message with both keyboards
    await update.message.reply_text(
        "Welcome to GTOPay! Choose an option below 👇\n\n" 
        "• Open payment portal\n" 
        "• Login or create account\n" 
        "• Get our Android app",
        reply_markup=reply_markup
    )
    
    # Send additional message with download button
    await update.message.reply_text(
        "Download our Android app for the best experience:",
        reply_markup=inline_markup
    )

def main():
    try:
        # Initialize bot
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start))
        
        # Start the bot
        logging.info("Bot started successfully")
        app.run_polling()
    except Exception as e:
        logging.error(f"Critical error occurred: {e}")
        raise

if __name__ == "__main__":
    start_keep_alive()
    main()