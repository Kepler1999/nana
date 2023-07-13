from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get("/main/")
async def main():
    return {'msg': 'ok'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
