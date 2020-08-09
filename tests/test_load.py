import datetime
import random
import socket
import time

from faker import Faker
fake = Faker()

base = '<190>Aug  9 12:45:13 ya-virtualbox nginx: {time_local}|1588184474.870|{remote_addr}|HTTP/1.1|GET|mhd.limehd.tv|/streaming/domashniy/324/vh1w/playlist.m3u8|-|206|4004|0.000|-|-|-|-|-|-|Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36 WebAppManager|-|1|1|{bytes_sent}'

base_pool = [base.format(time_local='{time_local}', remote_addr='{remote_addr}', bytes_sent=random.randrange(100, 1000000)) for _ in range(100)]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

c = 0
try:
    while True:
        end = time.time() + 1
        for _ in range(2000):
            time.sleep(0.0001)
            time_local = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%-S') + ' +0300'

            mess = random.choice(base_pool).format(time_local=time_local, remote_addr=fake.ipv4())
            sock.sendto(mess.encode(), ('localhost', 9999))
            # _ = sock.recv(8)
            c += 1
        delta = end - time.time()
        if delta > 0:
            time.sleep(delta)
        else:
            print(delta)
finally:
    print(f'CCC: {c}')
