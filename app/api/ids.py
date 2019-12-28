# Copyright (C) 2019 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


import uuid
from datetime import datetime
from secrets import token_urlsafe, token_hex, randbelow, randbits

from pydantic import BaseModel, Schema

from .app import app
from .data import data

DEFAULT_UUID_NAMESPACE = uuid.UUID('00000000-0000-0000-0000-000000000000')
TOKENS_SIZE = 32
RANDBITS_SIZE = 128
RANDINT = 999_999_999
MAX_48BIT = 281_474_976_710_655


class Counters(BaseModel):
    counter: int = Schema(..., example=1024, title="Overall unique counter")
    daily: int = Schema(..., example=128, title="Daily unique counter")
    hourly: int = Schema(..., example=64, title="Hourly unique counter")
    minutely: int = Schema(..., example=2, title="Minutely unique counter")


class UUIDs(BaseModel):
    uuid1: uuid.UUID = Schema(..., example="371abe38-293e-11ea-96ac-0da5d077f224", title="UUID1 with given node")
    uuid3: uuid.UUID = Schema(..., example="770fdca6-b84c-32e3-8aee-4f7aca5da38a",
                              title="UUID3 with given namespace and name")
    uuid4: uuid.UUID = Schema(..., example="4ba1927a-94a6-49b8-aea6-e3ccab22bc4b", title="UUID4 random UUIDs")
    uuid5: uuid.UUID = Schema(..., example="e297db46-8505-5009-ba39-aa2c8baedbb7",
                              title="UUID5 with given namespace and name")


class Time(BaseModel):
    iso: str = Schema(..., example="2019-12-28T06:49:37.743407", title="DateTime in ISO format")
    timestamp: int = Schema(..., example=1577508577, title="UNIX timestamp")
    date: int = Schema(..., example=20191228, title="Date in integer")
    time: int = Schema(..., example=64937, title="Time in integer")
    datetime: int = Schema(..., example=20191228064937, title="Date and Time in integer")
    year: int = Schema(..., example=2019, title="Year in integer")
    month: int = Schema(..., example=12, title="Month in integer")
    day: int = Schema(..., example=28, title="Day in integer")
    hour: int = Schema(..., example=6, title="Hour in integer")
    minute: int = Schema(..., example=49, title="Minute in integer")
    second: int = Schema(..., example=37, title="Second in integer")
    microsecond: int = Schema(..., example=743407, title="Microsecond in integer")


class Random(BaseModel):
    urlsafe: str = Schema(..., example="H-CjdOii4qIzQtzXEAnOUaIQLw9wxyA0LYafNPrATfs", title="Token usable to URLs")
    hex: str = Schema(..., example="50d6858ae562e0526c60cd4d66ca011981188ef8927c4de648fa7a614bc21add",
                      title="Token hex")
    integer: int = Schema(..., example=33532999, title="Random integer from 0 to given max")
    bits: str = Schema(..., example="4948411366347323230433518920752968098", title="128 bit random integer")


class IDs(BaseModel):
    counters: Counters = Schema(...)
    uuid: UUIDs = Schema(...)
    time: Time = Schema(...)
    random: Random = Schema(...)


class RequestParams(BaseModel):
    random_max_int: int = Schema(RANDINT, gt=1, le=MAX_48BIT, example=RANDINT, title="Max value for random integer.")
    uuid_node: int = Schema(None, ge=0, le=MAX_48BIT, example=1024, title="Node for uuid1 generator.")
    uuid_namespace: uuid.UUID = Schema(DEFAULT_UUID_NAMESPACE, example="2ed65488-204a-3714-ac63-072f63d1e5e1",
                                       title="Namespace for uuid3 and uuid5 generator.")
    uuid_name: str = Schema(None, example="idsaas", title="Name for uuid3 and uuid5 generators.")


@app.get('/api/v1/ids', response_model=IDs, tags=['IDs'])
async def ids_get() -> IDs:
    return await ids(RequestParams())


@app.post('/api/v1/ids', response_model=IDs, tags=['IDs'])
async def ids_post(params: RequestParams = None) -> IDs:
    return await ids(params if params else RequestParams())


async def ids(params: RequestParams) -> IDs:
    """Returns yours new IDs."""

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

    uuids = UUIDs(
        uuid1=uuid.uuid1(params.uuid_node if params.uuid_node else (randbits(48) | (1 << 40))),
        uuid3=uuid.uuid3(params.uuid_namespace, params.uuid_name if params.uuid_name else token_urlsafe(TOKENS_SIZE)),
        uuid4=uuid.uuid4(),
        uuid5=uuid.uuid5(params.uuid_namespace, params.uuid_name if params.uuid_name else token_urlsafe(TOKENS_SIZE)),
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
        urlsafe=token_urlsafe(TOKENS_SIZE),
        hex=token_hex(TOKENS_SIZE),
        integer=randbelow(params.random_max_int),
        bits=randbits(RANDBITS_SIZE),
    )

    return IDs(
        counters=counters,
        uuid=uuids,
        time=time,
        random=rnd,
    )
