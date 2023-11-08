@echo off
set a=%~n1
set b=%cd%
copy %b%\%a%.jpg %b%\photo\dist\file_001.jpg
cd photo\dist
call starmusic_v11.exe
copy %b%\photo\dist\star_sound.wav %b%\music\star_sound.wav
copy %b%\photo\dist\DTMF_data.csv %b%\tmp\DTMF_data.csv
del %b%\photo\dist\star_sound.wav
del %b%\photo\dist\DTMF_data.csv
cd %b%\music
start wav_to_mp3.bat