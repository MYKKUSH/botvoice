#!/bin/bash

# Скачиваем ffmpeg (если нужно)
mkdir -p bin
cd bin
curl -L -o ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz
tar -xf ffmpeg.tar.xz --strip-components=1
chmod +x ffmpeg
cd ..

# Добавляем ffmpeg в PATH
export PATH=$PWD/bin:$PATH

# Запуск бота
python bot.py
