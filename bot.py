import os
import speech_recognition as sr
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from pydub import AudioSegment

# Вставь сюда токен своего бота
TELEGRAM_TOKEN = '7798240839:AAEWV-BvjmOSoDL_8ixiW5eNllod7ZmJHkU'

def voice_handler(update: Update, context: CallbackContext):
    voice = update.message.voice
    file = context.bot.getFile(voice.file_id)
    
    ogg_path = f"voice.ogg"
    wav_path = f"voice.wav"

    file.download(ogg_path)

    try:
        # Конвертация OGG (Opus) -> WAV
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(wav_path, format="wav")

        # Распознавание
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ru-RU")

        update.message.reply_text(f"📝 Текст: {text}")

    except Exception as e:
        update.message.reply_text(f"⚠️ Ошибка: {str(e)}")
    
    finally:
        # Очистка
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
