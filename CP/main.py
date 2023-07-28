# This is an openapi project with fastapi
# To test model driven mode
# And to static data of app/website

from fastapi import FastAPI, Request

app = FastAPI()

# add config
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi import Limiter, _rate_limit_exceeded_handler

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


from model import db


# add blueprint
from service.routers import geography

app.include_router(geography.router)

from service.routers.school import digital_asset

app.include_router(digital_asset.router)


@limiter.limit("1/second")
@app.get("/test")
def print_hi(request: Request):
    # Get server status for test
    return {"server": "ON"}  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", reload=True)
