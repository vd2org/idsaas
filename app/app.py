# Copyright (C) 2019 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


from fastapi import FastAPI

app = FastAPI(
    title="idsaas.win",
    description="ISs as a Service.",
    version="edge",
)


@app.on_event('startup')
async def startup():
    # TODO: Load vars
    pass


@app.get('/')
async def root():
    # TODO: Root page
    pass


@app.get('/api/v1/ids')
@app.get('/api/v1/ids')
async def ids():
    # TODO: Return values
    pass
