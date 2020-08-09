import argparse
import asyncio
import sys
import time
import warnings
from typing import NamedTuple, Optional

import geoip2.database
import geoip2.errors
import syslogmp
from aioinflux import InfluxDBClient, InfluxDBError, lineprotocol, MEASUREMENT, TIMEINT, TAG, INT

OtherCountry = 'O1'
q = asyncio.Queue(maxsize=100000)


@lineprotocol 
class Point(NamedTuple):
    measurement: MEASUREMENT
    timestamp: TIMEINT
    country_id: TAG
    channel: TAG
    streaming_server: TAG
    quality: TAG
    value: INT


async def save(logs, influx, mmdb) -> None:

    def parse_(log: bytes, timestamp: int) -> Point:
        _data = syslogmp.parse(log)
        msg = _data.message.decode('utf8').split('|')

        try:
            code = mmdb.city(msg[2]).country.iso_code
        except geoip2.errors.AddressNotFoundError:
            code = None

        # /streaming/domashniy/324/vh1w/playlist.m3u8
        #            channel       quality
        uri = msg[6].split('/')
        channel, quality = uri[2], uri[4]

        bytes_sent = int(msg[-1])

        return Point(
            measurement='bytes_sent',
            timestamp=timestamp,  # _data.timestamp.isoformat() + 'Z',
            country_id=code or OtherCountry,
            channel=channel,
            streaming_server=msg[5],
            quality=quality,
            value=bytes_sent,
        )

    batch = []
    for log, timestamp in logs:
        try:
            batch.append(parse_(log, timestamp))
        except Exception:
            pass  # todo log

    await influx.write(batch)


async def parser(args) -> Optional[BaseException]:
    tasks = set()
    async with InfluxDBClient(host=args.influx_host, port=args.influx_port, db=args.influx_database) as influx:
        await influx.create_database(db=args.influx_database)

        with geoip2.database.Reader(args.maxmind) as mmdb:
            while True:
                tasks.add(
                    asyncio.ensure_future(
                        save([await q.get() for _ in range(100)], influx, mmdb)
                    )
                )
                done, tasks = await asyncio.wait(tasks, timeout=0, return_when=asyncio.FIRST_EXCEPTION)
                for task in done:
                    if isinstance(task.exception(), InfluxDBError):
                        # exit if there's an error in writing to the db
                        [t.cancel() for t in tasks]
                        await asyncio.wait(tasks)
                        return task.exception()


class SyslogProtocol:
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, log, addr):
        try:
            q.put_nowait((log, time.time_ns()))  # datetime.now()
        except asyncio.QueueFull:
            warnings.warn('The log queue has reached its maxsize.')
        # self.transport.sendto(b'0', addr)  # we don't need to respond back

    def connection_lost(self, *args):
        pass  # suppress server closed connection error


async def main(loop, args):
    print('Started syslog server')
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: SyslogProtocol(),
        local_addr=('localhost', args.port)
    )
    try:
        error = await parser(args)
        if error is not None:
            loop.stop()
            raise error
    finally:
        if not loop.is_closed():
            transport.close()


if __name__ == '__main__':
    cli = argparse.ArgumentParser()
    cli.add_argument('--port', default=514)  # I doubt that 514 should be the default port
    cli.add_argument('-i', '--influx-host', dest='influx_host', default='localhost')
    cli.add_argument('-d', '--influx-db', dest='influx_port', default='8086')
    cli.add_argument('--mt', dest='influx_database', default='bytes_sent')
    cli.add_argument('--maxmind', default='/usr/share/GeoIP/GeoLite2-City.mmdb')

    args = cli.parse_args()

    loop = asyncio.get_event_loop()
    task = loop.create_task(main(loop, args))
    try:
        loop.run_forever()
        if task.exception():
            sys.exit(repr(task.exception()))
    finally:
        loop.close()
