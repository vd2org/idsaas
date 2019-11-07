# Copyright (C) 2019 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


from datetime import datetime
from secrets import token_urlsafe, token_hex, randbelow, randbits
import uuid

from pydantic import BaseModel, Schema

from uvapp import app
from data import data

DEFAULT_UUID_NAMESPACE = uuid.UUID('00000000-0000-0000-0000-000000000000')
DEFAULT_TOKENS_SIZE = 32
DEFAULT_RANDBITS_SIZE = 128
DEFAULT_RANDINT = 999_999_999
MAX_48BIT = 281474976710655


class Counters(BaseModel):
    counter: int = Schema(..., title="Overall unique counter")
    daily: int = Schema(..., title="Daily unique counter")
    hourly: int = Schema(..., title="Hourly unique counter")
    minutely: int = Schema(..., title="Minutely unique counter")


class UUID(BaseModel):
    uuid1: str = Schema(..., title="UUID1 with given nodeid")
    uuid3: str = Schema(..., title="UUID3 with given namespace and name")
    uuid4: str = Schema(..., title="UUID4 random UUID")
    uuid5: str = Schema(..., title="UUID5 with given namespace and name")


class Time(BaseModel):
    iso: str = Schema(..., title="DateTime in ISO format")
    timestamp: int = Schema(..., title="UNIX timestamp")
    date: int = Schema(..., title="Date in integer")
    time: int = Schema(..., title="Time in integer")
    datetime: int = Schema(..., title="Date and Time in integer")
    year: int = Schema(..., title="Year in integer")
    month: int = Schema(..., title="Month in integer")
    day: int = Schema(..., title="Day in integer")
    hour: int = Schema(..., title="Hour in integer")
    minute: int = Schema(..., title="Minute in integer")
    second: int = Schema(..., title="Second in integer")
    microsecond: int = Schema(..., title="Microsecond in integer")


class Random(BaseModel):
    urlsafe: str = Schema(..., title="Token usable to URLs")
    hex: str = Schema(..., title="Token hex")
    integer: int = Schema(..., title="Random integer from 0 to given max")
    bits: int = Schema(..., title="Integer with size of given random")


class IDs(BaseModel):
    counters: Counters = Schema(...)
    uuid: UUID = Schema(...)
    time: Time = Schema(...)
    random: Random = Schema(...)


@app.get('/api/v1/ids')
@app.post('/api/v1/ids')
async def ids():
    """Returns yours new ids."""

    # TODO!!!
    # Process counters
    data.counter += 1
    data.daily += 1
    data.hourly += 1
    data.minutely += 1

    counters = Counters(
        counter=data.counter,
        daily=data.daily,
        hourly=data.hourly,
        minutely=data.minutely,
    )
    uuid.uuid1()
    uuids = UUID(
        uuid1=str(uuid.uuid1(randbits(48) | (1 << 40))),
        uuid3=str(uuid.uuid3(DEFAULT_UUID_NAMESPACE, token_urlsafe(DEFAULT_TOKENS_SIZE))),
        uuid4=str(uuid.uuid4()),
        uuid5=str(uuid.uuid5(DEFAULT_UUID_NAMESPACE, token_urlsafe(DEFAULT_TOKENS_SIZE))),
    )

    now = datetime.utcnow()
    date = now.year * 10000 + now.month * 100 + now.day
    time = now.hour * 10000 + now.minute * 100 + now.second

    time = Time(
        iso=now.isoformat(),
        timestamp=now.timestamp(),
        date=date,
        time=time,
        datetime=date * 1000000 + time,
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        second=now.second,
        microsecond=now.microsecond,
    )

    rnd = Random(
        urlsafe=token_urlsafe(DEFAULT_TOKENS_SIZE),
        hex=token_hex(DEFAULT_TOKENS_SIZE),
        integer=randbelow(DEFAULT_RANDINT),
        bits=randbits(DEFAULT_RANDBITS_SIZE),
    )

    return IDs(
        counters=counters,
        uuid=uuids,
        time=time,
        random=rnd,
    )
