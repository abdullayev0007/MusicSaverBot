import os
import instaloader
from pytube import YouTube
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # <--- BU YERGA BOTFATHER'DAN OLGAN TOKENNI YOZASIZ

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎧 Salom! Men sizga yordam beraman:\n\n"
        "📸 Instagram video yoki reel link yuboring — men uni yuklab beraman.\n"
        "🎵 YouTube link yuboring — men uni MP3 qilib beraman.\n\n"
        "👇 Link yuboring:"
    )

def download_youtube(update: Update, url):
    try:
        update.message.reply_text("⏳ Yuklanmoqda... kuting iltimos.")
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(filename="music.mp3")
        update.message.reply_audio(audio=open("music.mp3", "rb"), title=yt.title)
        os.remove("music.mp3")
    except Exception as e:
        update.message.reply_text(f"⚠️ Xatolik: {e}")

def download_instagram(update: Update, url):
    try:
        update.message.reply_text("⏳ Instagram video yuklanmoqda...")
        bot = instaloader.Instaloader(dirname_pattern="downloads", save_metadata=False)
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(bot.context, shortcode)
        bot.download_post(post, target="downloads")
        for f in os.listdir("downloads"):
            if f.endswith(".mp4"):
                video_path = os.path.join("downloads", f)
                update.message.reply_video(video=open(video_path, "rb"))
                os.remove(video_path)
        for f in os.listdir("downloads"):
            os.remove(os.path.join("downloads", f))
        os.rmdir("downloads")
    except Exception as e:
        update.message.reply_text(f"⚠️ Instagram yuklashda xatolik: {e}")

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if "youtube.com" in text or "youtu.be" in text:
        download_youtube(update, text)
    elif "instagram.com" in text:
        download_instagram(update, text)
    else:
        update.message.reply_text("📩 Iltimos, Instagram yoki YouTube link yuboring.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
