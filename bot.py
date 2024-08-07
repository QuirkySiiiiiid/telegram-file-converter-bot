import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me a video file to convert.')

def handle_document(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file.download('input_video.mp4')  # Save the uploaded file

    # Perform conversion
    os.system('ffmpeg -i input_video.mp4 output_video.mkv')  # Example conversion

    # Send the converted file
    with open('output_video.mkv', 'rb') as video:
        update.message.reply_document(document=video, caption='Converted Video')

def main() -> None:
    updater = Updater(TELEGRAM_API_KEY)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("video/mp4"), handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
