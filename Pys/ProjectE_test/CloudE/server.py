from fastapi import FastAPI

app = FastAPI()   


from service.routers import place
app.include_router(place.router)

@app.get('/home')
async def home():
    return ({"msg":1})



if __name__ == '__main__':
    # db.generate_mapping()
    import uvicorn
    uvicorn.run(app="server:app",reload=True)