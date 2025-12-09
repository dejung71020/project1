from fastapi import APIRouter
from pydantic import BaseModel
import requests
import os

router = APIRouter(prefix="/chat", tags=["chat"])

# 환경 변수에서 가져오기
API_URL = os.getenv("API_URL") #OpenAI API
API_KEY = os.getenv("API_KEY")

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-5-nano",  # 사용할 모델 
        "messages": [{"role": "user", "content": req.message}]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    print(response.status_code)
    print(response.json())  # 응답 전체 확인

    if "choices" in response.json():
        bot_reply = response.json()["choices"][0]["message"]["content"]
    else:
        bot_reply = response.json().get("error", {}).get("message", "API 호출 실패")

    return {"reply": bot_reply}
