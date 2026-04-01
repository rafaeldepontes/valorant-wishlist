from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter

origins = [
    "*",
]

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    max_age=300,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["Accept", "Content-Type"],
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    )

'''
This has a rate limit of 20 request per
minute and this should be or default value
through the application.
'''
@app.get("/")
@limiter.limit("20/minute")
async def read_root(request: Request):
    print(request)
    return {"Hello": "World"}