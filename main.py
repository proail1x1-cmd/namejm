from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import datetime

app = FastAPI(
    title="Public FastAPI Example",
    description="🎉 API عامة يمكن لأي شخص استخدامها أو تطويرها",
    version="1.0.0"
)

# السماح بالاتصال من أي مكان (API عامة)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تحميل البيانات من ملف JSON
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# الصفحة الرئيسية
@app.get("/")
def home():
    return {
        "message": "مرحبًا بك في الـ Public API 🎉",
        "endpoints": ["/users", "/users/{id}", "/add"],
        "author": "Your Name",
        "version": "1.0.0",
    }

# عرض كل المستخدمين
@app.get("/users")
def get_users():
    data = load_data()
    return data

# عرض مستخدم حسب ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    data = load_data()
    user = next((u for u in data if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# إضافة مستخدم جديد
@app.post("/add")
def add_user(user: dict):
    data = load_data()
    user["id"] = len(data) + 1
    user["created_at"] = datetime.datetime.now().isoformat()
    data.append(user)
    save_data(data)
    return {"message": "تمت الإضافة بنجاح ✅", "user": user}