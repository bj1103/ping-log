import logging
from logging.handlers import TimedRotatingFileHandler
import os 
from time import sleep

# intranet, gateway, internet public ip
ip_list = ['140.112.30.130', '140.112.30.254', '8.8.8.8'] #for csman1, csman2, dns1, dns2
# ip_list = ['10.217.44.51', '10.217.44.254', '8.8.8.8'] #for SA-dns1, SA-dns2
# path = '/var/log/ping.log'
path = './ping.log'

_log_format = "%(asctime)s - [%(levelname)5s] - %(message)s"

def get_file_handler(log_path):
    file_handler = TimedRotatingFileHandler(filename=log_path, when='D', interval=1, backupCount=7, encoding='utf-8', delay=False)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler

def get_logger(name, log_path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(log_path))
    # logger.addHandler(get_stream_handler())
    return logger


def ping(ip_list):
    for ip in ip_list:
        output = os.popen('ping {} -c 1 -W 2'.format(ip)).read()
        index = output.find('transmitted')
        transmited = output[index+13:index+14]
        if transmited != '1':
            logger.error("ping {:15s} failed".format(ip))
        else: 
            logger.info("ping {:15s} succeeded".format(ip))

if __name__ == '__main__':
    logger = get_logger(__name__, path)
    while True:
        ping(ip_list)
        sleep(10)