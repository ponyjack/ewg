from datetime import datetime
from string import Template
import subprocess
import requests
from loguru import logger
import socket
import schedule

import time


def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            data = response.json()
            return data["ip"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while fetching external IP: {e}")


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        return s.getsockname()[0]
    except Exception:
        logger.error("Couldn't get local IP")


def restart_wg_service(ip):

    now = datetime.now()
    month = now.month
    if month > 10:
        month = month - 10
    day = now.day
    port = f"{month}{day}"

    with open("docker-compose.yaml.tpl", "r") as f:
        data = f.read()
        template = Template(data)
        data2 = template.substitute(host_ip=ip, udp_port=port)
        logger.info(data2)
        with open("docker-compose.yml", "w") as f:
            f.write(data2)

    try:
        output = subprocess.check_output("docker-compose down", shell=True)
        logger.info(output)
    except Exception:
        logger.error("Error occurred while restarting wg service")

    try:
        logger.warning("starting wg service {} {}", ip, port)
        output = subprocess.check_output("docker-compose up -d", shell=True)
        logger.info(output)
    except Exception:
        logger.error("Error occurred while restarting wg service")


def main():
    ip = get_external_ip()
    if not ip:
        ip = get_local_ip()
        if not ip:
            logger.error("Couldn't get local IP")
            return
    restart_wg_service(ip)
    schedule.every().day.at("03:00", "Asia/Shanghai").do(restart_wg_service, ip=ip)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
