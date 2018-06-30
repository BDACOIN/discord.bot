%~d0
cd %~d0%~p0

python -m pip install --upgrade pip
python -m pip install -U discord.py
python -m pip install requests

:LOOP_LABEL
python DiaTanBot.py
timeout 2
goto :LOOP_LABEL