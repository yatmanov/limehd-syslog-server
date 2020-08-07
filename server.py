import asyncio
import json
import random
import socketserver
from datetime import datetime
from typing import Optional

from aioinflux import InfluxDBClient
# from influxdb import InfluxDBClient
from syslogmp import parse


CLIENT: Optional[InfluxDBClient] = None


# async def save(data):
    # async with InfluxDBClient(db='testdb') as client:
    #     await client.create_database(db='testdb')
    # await CLIENT.write(data)


class SysLogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = self.request[0].strip()
        socket = self.request[1]

        _data = parse(data)
        socket.sendto(b'', self.client_address)

        parts = _data.message.decode('utf8').split('|')

        ip = parts[2]
        streaming_server = parts[5]
        channel = parts[6].split('/')[1]
        quality = parts[6].split('/')[-2]

        point = [{
            'measurement': 'bytes_sent',
            'tags': {
                'country_id': ip,
                'channel': channel,
                'streaming_server': streaming_server,
                'quality': quality,
            },
            # 'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'time': datetime.now().isoformat() + 'Z',
            'fields': {
                # 'value': int(parts[-1])
                'value': random.randrange(0, 100000),
            }
        }]
        # loop = asyncio.get_running_loop()
        # print(CLIENT)
        asyncio.ensure_future(CLIENT.write(point[0]))
        # CLIENT.write_points(point)

        # print(json.dumps(point))


async def serve():
    global CLIENT
    async with InfluxDBClient(db='testdb') as client:
        CLIENT = client
        await client.create_database(db='testdb')

    host, port = 'localhost', 9999
    with socketserver.UDPServer((host, port), SysLogUDPHandler) as server:
        server.serve_forever()


if __name__ == '__main__':
    # client = InfluxDBClient(database='testdb')
    # client.create_database('testdb')
    # CLIENT = client

    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve())

