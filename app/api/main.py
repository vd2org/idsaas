# Copyright (C) 2019 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


import uvicorn

from uvapp import app
import root
import ids


def _keep():
    """Prevents pycharm to remove imports."""

    _ = root
    _ = ids


if __name__ == "__main__":
    uvicorn.run(app, debug=True, reload=True)
