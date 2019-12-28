# Copyright (C) 2019 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


import os

from fastapi import FastAPI

from . import counter

app = FastAPI(
    title="idsaas.win",
    description="ISs as a Service.",
    version="edge",
)


@app.on_event('startup')
async def startup():
    counter.data.host = os.environ['COUNTER_HOST']
