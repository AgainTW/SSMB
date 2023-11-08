@echo off
cd..
set b=%cd%
cd %b%\music\ffmpeg-20191111-20c5f4d-win64-static\bin
ffmpeg -i %b%\music\star_sound.wav %b%\music\star_sound.mp3
copy %b%\music\star_sound.mp3 %b%\product\star_sound.mp3
del %b%\music\star_sound.mp3
exit