import argparse
import asyncio
import socketserver

from aioinflux import InfluxDBClient
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError


def get_city(ip: str, path: str) -> str:
    # todo don't connect to db for each ip
    with Reader(path) as reader:
        try:
            response = reader.city(ip)
            return response.country.iso_code
        except AddressNotFoundError:
            return ''


async def save():
    async with InfluxDBClient(db='testdb') as client:
        await client.create_database(db='testdb')
        points = {
            'country_id',
            'channel',
            'streaming_server',
            'quality'
        }
        await client.write(points)


async def serve():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', default=514, help='port to listen')
    parser.add_argument('-i', default='http://localhost')
    parser.add_argument('-d', default='8086')
    # parser.add_argument('-n', default='testdb')  # do I need to know table name to write data?
    parser.add_argument('-mt', default='bytes_sent')
    parser.add_argument('-maxmind', default='/usr/share/GeoIP/GeoLite2-City.mmdb')

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve())
