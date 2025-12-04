import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from routers import auth, memos
from database import Base, engine

# .env 파일 로드
load_dotenv()

app = FastAPI()

# 환경 변수에서 SECRET_KEY 가져오기
SECRET_KEY = os.getenv("SECRET_KEY")

# (선택 사항) 키가 없을 경우를 대비한 기본값 설정 (혹은 에러 처리)
if not SECRET_KEY:
    SECRET_KEY = "default-secret-key" # 혹은 raise ValueError("SECRET_KEY missing")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(auth.router)
app.include_router(memos.router)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about")
async def about():
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}