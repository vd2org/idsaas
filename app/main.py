# Copyright (C) 2019 by Vd.
# This file is part of IDsaaS, ISs as a Service.
# IDsaaS is released under the MIT License (see LICENSE).


import uvicorn

from app import app

if __name__ == "__main__":
    uvicorn.run(app, debug=True, reload=True)
