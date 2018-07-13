%~d0
cd %~d0%~p0

python -m pip install --upgrade pip
python -m pip install -U discord.py
python -m pip install requests
python -m pip install base58

:LOOP_LABEL
python SwapPostBot.py
timeout 2
goto :LOOP_LABEL