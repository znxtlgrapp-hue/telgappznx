import os
import threading
from flask import Flask, render_template_string, send_from_directory
import telebot

# توكن البوت الخاص بك
TOKEN = "8354916035:AAEaUHOrkzciEMWyL_loALuRdbDGG1ee6bQ"
bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SONGS_FOLDER = os.path.join(BASE_DIR, "songs")

if not os.path.exists(SONGS_FOLDER):
    os.makedirs(SONGS_FOLDER)

app = Flask(__name__)

# واجهة التطبيق المصغر لتيليجرام
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Music App</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            background-color: var(--tg-theme-bg-color, #18222d);
            color: var(--tg-theme-text-color, #ffffff);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .header {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #2481cc;
        }
        .player-box {
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            box-sizing: border-box;
            text-align: center;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .now-playing {
            font-size: 16px;
            margin-bottom: 10px;
            font-weight: 500;
        }
        audio {
            width: 100%;
            height: 40px;
        }
        .song-list {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .song-card {
            background: #232e3c;
            padding: 12px 16px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        .play-btn {
            background: #2481cc;
            color: #ffffff;
            border: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="header">🎧 مشغل الأغاني</div>

    <div class="player-box">
        <div class="now-playing" id="trackName">اختر أغنية للتشغيل</div>
        <audio id="audioPlayer" controls autoplay></audio>
    </div>

    <div class="song-list">
        {% for song in songs %}
        <div class="song-card" onclick="playSong('{{ song.file }}', '{{ song.name }}')">
            <span>🎵 {{ song.name }}</span>
            <button class="play-btn">تشغيل</button>
        </div>
        {% endfor %}
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();

        const player = document.getElementById('audioPlayer');
        const trackName = document.getElementById('trackName');

        function playSong(file, name) {
            trackName.innerText = "تشغيل: " + name;
            player.src = "/songs/" + encodeURIComponent(file);
            player.play();
        }

        window.onload = () => {
            const firstSong = document.querySelector('.song-card');
            if (firstSong) {
                firstSong.click();
            }
        };
    </script>
</body>
</html>
"""

def get_songs_data():
    if not os.path.exists(SONGS_FOLDER):
        return []
    files = sorted([f for f in os.listdir(SONGS_FOLDER) if f.lower().endswith(".mp3")])
    return [{"file": f, "name": os.path.splitext(f)[0]} for f in files]

@app.route('/')
def home():
    songs = get_songs_data()
    return render_template_string(HTML_PAGE, songs=songs)

@app.route('/songs/<path:filename>')
def serve_audio(filename):
    return send_from_directory(SONGS_FOLDER, filename)

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(
        message.chat.id,
        "مرحباً بك! 👋\nاضغط على **الزر الأزرق بالأسفل** لتشغيل الأغاني مباشرة."
    )

def run_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    threading.Thread(target=run_server).start()
    bot.infinity_polling()
