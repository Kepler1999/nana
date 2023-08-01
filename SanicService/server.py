from SanicService import app
from sanic.response import json

# for server status
@app.get("/status")
def index(request):
    return json({"server": "ON"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, dev=True)
