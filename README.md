# 🛒 애완용품샵 — 반려동물 이커머스 백엔드

> 반려동물 용품 이커머스 백엔드. FastAPI REST API 설계부터 AI 챗봇 연동, 5명 팀의 첫 협업 프로젝트.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_RDS-FF9900?style=flat-square&logo=amazonaws&logoColor=white)

---

## 📌 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 기간 | 2025.12 – 2026.01 (1.5개월) |
| 팀 구성 | 5명 |
| 담당 | 백엔드 개발 |
| 아키텍처 | MVC (Flat Structure) |

---

## 🛠 기술 스택

| 분류 | 기술 |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | MySQL, AWS RDS |
| AI | OpenAI GPT-4.1-mini |
| Auth | Session 기반 (SessionMiddleware) |
| ML | Scikit-learn (RandomForest 추천 시스템) |
| Data | Selenium 크롤러 |

---

## ✨ 핵심 구현

### 1. 주문 / 재고 트랜잭션 원자성 보장

결제 · 재고 차감 · 주문 기록이 개별 처리될 경우, 서버 다운 시 데이터 불일치가 발생할 수 있습니다.

**해결:** 하나의 트랜잭션으로 묶어 처리 — 실패 시 전체 롤백

```python
def create_order(db: Session, user_id: int, items: List[Dict]):
    try:
        # 1. 재고 확인
        # 2. 주문서 생성 (Orders)
        # 3. 상세 품목 기록 (Order_Items)
        # 4. 재고 차감 + 판매수 증가
        db.commit()
        return order_id
    except Exception as e:
        db.rollback()
        raise e
```

**결과:** 데이터 불일치 0건 유지

### 2. OpenAI 챗봇 환각 차단

OpenAI API를 연동한 고객센터 챗봇이 사이트와 무관한 질문에도 답변하는 환각 현상이 발생했습니다.

**해결:** 예상 Q&A 50개를 JSON으로 구조화 → system_prompt에 전체 주입 → 관련 없는 질문은 모두 거절

```python
faq_context = "\n".join([f"Q: {item['question']} A: {item['answer']}"
                          for item in faq_data])

system_prompt = (
    "너는 특정사이트 고객센터 직원이다. "
    "반드시 아래 FAQ와 정책을 기반으로 답변하라.\n"
    f"{faq_context}"
)
```

**장점:** 별도 DB 없이 간단하게 환각 현상 제어

### 3. AWS RDS로 팀 DB 환경 통일

로컬 MySQL 대신 AWS RDS를 도입해 5명 전원이 동일한 DB 환경에서 개발

### 4. 랜덤포레스트 추천 시스템

```
recommend/
├── recommend.py   # RandomForest 학습
└── batch.py       # 시간별 배치 재학습
```

---

## 🗄 DB 구조

```
users        사용자 정보, 세션 인증
products     상품 정보, 카테고리, 재고
orders       주문 정보 (총금액)
order_items  주문 상세 품목
carts        장바구니 (로그아웃 후에도 유지)
reviews      상품 리뷰
memo         게시글 (CRUD)
```

---

## 📡 API 명세

| 도메인 | 엔드포인트 |
|---|---|
| Auth | POST /auth/signup, /auth/login, /auth/logout |
| Products | GET /products, GET /products/{id}, POST /products/{id}/review |
| Cart | POST /cart/add, GET /cart, DELETE /cart/remove/{id} |
| Orders | POST /orders/buy/{id}, GET /orders/detail/{id} |
| Memos | GET/POST /memos, PUT/DELETE /memos/{id} |
| Chat | POST /chat |

---

## 🚀 실행 방법

```bash
git clone https://github.com/dejung71020/project1.git
cd project1

pip install -r requirements.txt

# .env 설정 (DATABASE_URL, SECRET_KEY, OPENAI_API_KEY)
uvicorn main:app --reload
```

---

## 📁 프로젝트 구조

```
├── main.py          # 앱 진입점, 페이지 라우트 (/, /login, /mypage)
├── database.py      # SQLAlchemy 엔진, Base
├── dependencies.py  # get_db(), 비밀번호 해싱
├── schemas.py       # Pydantic 모델
├── routers/         # auth, products, cart, orders, memos, chatbot
├── data/            # DAO 레이어 (raw SQL via sqlalchemy.text())
├── recommend/       # RandomForest 학습 + 배치
└── templates/       # Jinja2 HTML (SSR)
```
