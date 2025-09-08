from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.models import Base, db_helper
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code is run before app is launched
    # create transaction
    async with db_helper.engine.begin() as conn:
        # Create all DB tables based on models
        await conn.run_sync(Base.metadata.create_all)
        # await conn.run_sync(Base.metadata.drop_all)
    # This code is run after app is finished
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }
