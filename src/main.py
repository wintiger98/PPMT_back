from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, projects

app = FastAPI()

app.include_router(auth.router)
app.include_router(projects.router)

# CORS 설정 추가
origins = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
]  # 허용할 출처를 여기에 추가

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
