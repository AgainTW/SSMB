@echo off
set a=%~n1
set b=%cd%
copy %b%\%a%.jpg %b%\photo\file_001.jpg
cd %b%\photo
python starmusic_v11.py
copy %b%\photo\star_sound.wav %b%\music\star_sound.wav
copy %b%\photo\DTMF_data.csv %b%\tmp\DTMF_data.csv
del %b%\photo\star_sound.wav
del %b%\photo\DTMF_data.csv
cd %b%\music
start wav_to_mp3.bat