python -m pip install loguru requests

nohup python main.py >output.log 2>&1 &
tail -f output.log
