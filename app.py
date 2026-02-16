import os
import logging
import threading
import gradio as gr
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai
from httpx import AsyncClient, Timeout

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tognon est enfin là ! Pose-moi ta question.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Erreur Gemini: {e}")
        await update.message.reply_text("Désolé, j'ai eu un petit problème technique.")

def run_bot():
    # Correction de la syntaxe du Timeout pour httpx
    custom_timeout = Timeout(60.0, connect=60.0)
    
    # On crée l'application avec les bons réglages de délai
    application = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .connect_timeout(60.0)
        .read_timeout(60.0)
        .write_timeout(60.0)
        .build()
    )
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Démarrage du polling Telegram...")
    application.run_polling(stop_signals=False)

if __name__ == "__main__":
    # Lancement du bot
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Interface Gradio
    demo = gr.Interface(
        fn=lambda x: "Bot Tognon : Opérationnel sur Telegram", 
        inputs="text", 
        outputs="text",
        title="Tognon Status"
    )
    demo.launch(server_name="0.0.0.0", server_port=7860)