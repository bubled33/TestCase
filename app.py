import uvicorn
from fastapi import FastAPI

from config import settings
from handlers import *

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.Server.host, port=settings.Server.port)
