apt update
apt install -y python3-pip
python3 -m pip install loguru requests

nohup python3 main.py >output.log 2>&1 &
