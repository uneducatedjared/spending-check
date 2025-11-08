from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # 1. Import the middleware
from .utils.common import create_unified_response
from .config.database import engine
from .models import models
from .endpoints import auth as auth_router
from .endpoints import tickets as tickets_router
from .endpoints import employees as employees_router


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080", 
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins to make requests
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    捕获 HTTPException, 并用统一的响应格式返回。
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=create_unified_response(
            code=exc.status_code,
            detail=exc.detail,
            data=None
        ),
    )
    
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


app.include_router(auth_router.router)
app.include_router(tickets_router.router, prefix="/tickets")
app.include_router(employees_router.router, prefix="/employees")