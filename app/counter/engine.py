# Copyright (C) 2019 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


import asyncio
import io
import logging
import os
import pickle
import signal
from contextlib import suppress
from datetime import datetime, timezone
from time import time

logging.basicConfig(format='%(asctime)s - %(levelname)-5s - %(name)-5s: %(message)s')

logger = logging.getLogger('engine')
logger.setLevel(logging.INFO)

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24
DT_NOW = datetime.utcnow()


def start_day(n): return datetime(n.year, n.month, n.day, tzinfo=timezone.utc).timestamp()


def start_hour(n): return datetime(n.year, n.month, n.day, n.hour, tzinfo=timezone.utc).timestamp()


def start_minute(n): return datetime(n.year, n.month, n.day, n.hour, n.minute, tzinfo=timezone.utc).timestamp()


class data:
    counter: int = 0
    daily: int = 0
    hourly: int = 0
    minutely: int = 0

    first_daily_req = start_day(DT_NOW)
    first_hourly_req = start_hour(DT_NOW)
    first_minutely_req = start_minute(DT_NOW)

    @classmethod
    def inc(cls):
        now = time()

        cls.counter += 1

        if now - cls.first_daily_req >= DAY:
            cls.first_daily_req = now
            cls.daily = 0
        else:
            cls.daily += 1

        if now - cls.first_hourly_req >= HOUR:
            cls.first_hourly_req = now
            cls.hourly = 0
        else:
            cls.hourly += 1

        if now - cls.first_minutely_req >= MINUTE:
            cls.first_minutely_req = now
            cls.minutely = 0
        else:
            cls.minutely += 1


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while True:
            await reader.readline()

            data.inc()

            f = f"{data.counter} {data.daily} {data.hourly} {data.minutely}\n"

            writer.write(f.encode())
            await writer.drain()
    except ConnectionError:
        return
    finally:
        with suppress(Exception):
            writer.close()
            await writer.wait_closed()


def load(file):
    with io.FileIO(file) as f:
        (data.counter, data.daily, data.hourly, data.minutely,
         data.first_daily_req, data.first_hourly_req, data.first_minutely_req) = pickle.load(f)


def save(file):
    with io.FileIO(file, 'w') as f:
        pickle.dump((data.counter, data.daily, data.hourly, data.minutely,
                     data.first_daily_req, data.first_hourly_req, data.first_minutely_req), f)


async def saver(freq, file):
    try:
        while True:
            await asyncio.sleep(freq)
            save(file)
    except asyncio.CancelledError:
        return
    except:
        logger.warning('Can\'t save state to file `%s`!', file)
        logger.exception('Got exception:')
    finally:
        save(file)


def main():
    port = int(os.environ.get('PORT', 8888))
    file = os.environ.get('FILE', './counters.p')
    saver_freq = int(os.environ.get('SAVER_FREQ', 60))

    try:
        load(file)
    except:
        logger.warning('Can\'t load state from file `%s`, using default values!', file)
        logger.exception('Got exception:')

    logger.info('Starting counting server on port `%s`...', port)

    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(asyncio.start_server(handle, '0.0.0.0', port))

    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(s, loop.stop)
        except NotImplementedError:
            signal.signal(s, lambda sig, frame: loop.stop())

    loop.create_task(saver(saver_freq, file))

    loop.call_soon(lambda: logger.info("Working..."))
    loop.run_forever()

    logger.info("Going down...")

    server.close()
    try:
        loop.run_until_complete(server.wait_closed())
    except ConnectionError:
        pass

    pending = asyncio.Task.all_tasks()
    for t in pending:
        if not t.done():
            t.cancel()

    with suppress(asyncio.CancelledError):
        loop.run_until_complete(asyncio.gather(*pending))

    loop.close()

    logger.info("Bye!")
