# Copyright (C) 2019-2022 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


from starlette.responses import Response

from .app import app

ROOT_PAGE = """
<html>
    <body>
        <h1>Yay! The IDs as a service!</h1>
        <p>See api docs <a href="/docs">here</a> or <a href="/redoc">here</a>!</p>
        
        <p>Source code available <a target='_blank' href='https://github.com/vd2org/idsaas'>here</a>.</p>
    </body>
</html>
"""


@app.get('/', responses={200: {'content-type': 'text/html'}}, include_in_schema=False)
def root():
    """\
    Returns home page.
    """

    return Response(content=ROOT_PAGE, media_type="text/html")
