from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models import User, Memo
from schemas import MemoCreate, MemoUpdate
from dependencies import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/memos", tags=["memos"])
templates = Jinja2Templates(directory="templates")

@router.post("/")
async def create_memo(request: Request, memo: MemoCreate, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authorized")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_memo = Memo(user_id=user.id, title=memo.title, content=memo.content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return new_memo

@router.get("/")
async def list_memos(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not authorized")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    memos = db.query(Memo).filter(Memo.user_id == user.id).all()
    return templates.TemplateResponse("memos.html", {"request": request, "memos": memos, "username": username})

@router.put("/{memo_id}")
async def update_memo(request: Request, memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    username = request.session.get("username")
    user = db.query(User).filter(User.username == username).first()
    db_memo = db.query(Memo).filter(Memo.id == memo_id, Memo.user_id == user.id).first()
    if not db_memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    if memo.title: db_memo.title = memo.title
    if memo.content: db_memo.content = memo.content
    db.commit()
    db.refresh(db_memo)
    return db_memo

@router.delete("/{memo_id}")
async def delete_memo(request: Request, memo_id: int, db: Session = Depends(get_db)):
    username = request.session.get("username")
    user = db.query(User).filter(User.username == username).first()
    db_memo = db.query(Memo).filter(Memo.id == memo_id, Memo.user_id == user.id).first()
    if not db_memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    db.delete(db_memo)
    db.commit()
    return {"message": "Memo deleted"}