import os
import whisper
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from pydub import AudioSegment

# Вставь сюда токен своего бота
TELEGRAM_TOKEN = ''

# Загружаем модель Whisper один раз
model = whisper.load_model("base")  # можно заменить на "small", "medium", "large" — точнее, но медленнее

def voice_handler(update: Update, context: CallbackContext):
    voice = update.message.voice
    file = context.bot.getFile(voice.file_id)
    
    ogg_path = "voice.ogg"
    wav_path = "voice.wav"

    file.download(ogg_path)

    try:
        # Конвертация OGG -> WAV
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(wav_path, format="wav")

        # Распознавание через Whisper
        result = model.transcribe(wav_path, language="ru")
        text = result["text"]

        update.message.reply_text(f"📝 Текст: {text}")

    except Exception as e:
        update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

    finally:
        # Очистка временных файлов
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.voice, voice_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
