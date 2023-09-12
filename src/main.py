from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, projects, project_contents

app = FastAPI()

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(project_contents.router)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:80",
]

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
