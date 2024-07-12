apt update
apt install pip3
python3 -m pip install loguru requests

nohup python3 main.py >output.log 2>&1 &
