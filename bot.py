import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

# Initialize Flask app
app = Flask(__name__)
bot = Bot(token=TELEGRAM_API_KEY)
dispatcher = Dispatcher(bot, None, use_context=True)

# Define command handler functions
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

# Add handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.document.mime_type("video/mp4"), handle_document))

# Define webhook route
@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), bot)
        dispatcher.process_update(update)
        return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
