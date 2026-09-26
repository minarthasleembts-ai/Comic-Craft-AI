from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="ComicCraft",
    version="1.0.0",
    description="AI Comic Story Creator"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.state.templates = templates

app.include_router(router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ComicCraft"
    }