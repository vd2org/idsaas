# Copyright (C) 2019 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


import asyncio
from contextlib import suppress
from dataclasses import dataclass


@dataclass(frozen=True)
class Counters:
    counter: int
    daily: int
    hourly: int
    minutely: int


class data:
    host: str = None
    port: int = 8888
    reader: asyncio.StreamReader = None
    writer: asyncio.StreamWriter = None


async def get_counters() -> Counters:
    try:
        if not data.reader or not data.writer:
            data.reader, data.writer = await asyncio.open_connection(data.host, data.port)

        data.writer.write(b'\n')
        await data.writer.drain()

        response = await data.reader.readline()

        return Counters(*[int(c) for c in response.split()])

    except asyncio.CancelledError:
        raise
    except:
        w = data.writer
        data.writer = None
        data.reader = None
        with suppress(Exception):
            w.close()

        raise ConnectionError
