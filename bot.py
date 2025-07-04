import os
import torch
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from transformers import AutoTokenizer, AutoModelForTokenClassification, TokenClassificationPipeline
from keep_alive import keep_alive  # ✅ добавлено

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # ✅ из переменной окружения

MODEL_NAME = "RUPunct/RUPunct_small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)
punct_pipeline = TokenClassificationPipeline(
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="first",
    device=0 if torch.cuda.is_available() else -1
)

def restore_punctuation(text: str) -> str:
    tokens = punct_pipeline(text)
    result = ""
    for token in tokens:
        word = token["word"]
        label = token["entity_group"]
        if label == "LOWER_COMMA":
            word += ","
        elif label == "LOWER_PERIOD":
            word += "."
        elif label == "LOWER_QUESTION":
            word += "?"
        elif label == "LOWER_VOSKL":
            word += "!"
        result += word + " "
    return result.strip()

def voice_handler(update: Update, context: CallbackContext):
    voice = update.message.voice
    file = context.bot.getFile(voice.file_id)

    ogg_path = "voice.ogg"
    wav_path = "voice.wav"

    file.download(ogg_path)

    try:
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(wav_path, format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            raw_text = recognizer.recognize_google(audio_data, language="ru-RU")

        punctuated_text = restore_punctuation(raw_text)
        update.message.reply_text(f"📝 {punctuated_text}")

    except Exception as e:
        update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

    finally:
        for f in (ogg_path, wav_path):
            if os.path.exists(f):
                os.remove(f)

def main():
    keep_alive()  # ✅ добавлено
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
