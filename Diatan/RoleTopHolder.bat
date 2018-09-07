%~d0
cd %~d0%~p0
:LOOP_LABEL
python RoleTopHolder.py
timeout 2
goto :LOOP_LABEL