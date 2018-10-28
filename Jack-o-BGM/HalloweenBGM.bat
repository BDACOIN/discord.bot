%~d0
cd %~d0%~p0

python -m pip install -U pip
python -m pip install -U discord.py
python -m pip install requests
python -m pip install -U youtube_dl

:LOOP_LABEL
python HalloweenBGM.py
timeout 2
goto :LOOP_LABEL