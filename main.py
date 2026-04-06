from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from database import get_connection, init_db
init_db()
app = FastAPI()
users=[]
valid_role=["viewer","analyst","admin"]
class user(BaseModel):
    name:str
    email:str
    password:str
    role:str
@app.post("/users")
def create_user(user:user):
    if user.role.lower() not in valid_role:
        raise HTTPException(status_code=400,detail="Invalid role")
    for i in users:
        if i["email"]==user.email:
            raise HTTPException(status_code=400,detail="Email already exist")
    new_user={
        "id":len(users)+1,
        "name":user.name,
        "email":user.email,
        "password":user.password,
        "role":user.role.lower(),
        "status":"active"
            }
    users.append(new_user)
    return {"message":"User created","user":new_user}
@app.get("/user")
def get_user():
    return users
@app.put("/user/{user_id}/role")
def update_role(user_id:int,role:str):
    if role.lower() not in valid_role:
        raise HTTPException(status_code=400,detail="Invalid role")
    for i in users:
        if i["id"]==user_id:
            i["role"]=role.lower()
            return {"message":"Role updated","user":i}
        raise HTTPException(status_code=404,detail="User not found")
@app.put("/user/{user_id}/status")
def update_status(user_id:int,status:str):
    if status.lower() not in ["active","Inactive"]:
        raise HTTPException(status_code=400,detail="Invalid status")
    for u in users:
        if u["id"]==user_id:
            u["status"]=status.lower()
            return {"message":"Status updated","user":u}
    raise HTTPException(status_code=404,detail="User not found")
record_store = []
record_id_counter = 1
valid_type = ["income", "expense"]
class Record(BaseModel):
    amount: float
    type: str
    category: str
    date: str
    description: str
    user_id: int
@app.post("/records")
def create_record(record: Record):
    global record_id_counter
    if record.type.lower() not in valid_type:
        raise HTTPException(status_code=400, detail="invalid type")
    user_found = None
    for u in users:
        if u["id"] == record.user_id:
            user_found = u
            break
    if not user_found:
        raise HTTPException(status_code=404, detail="user not found")
    if user_found["status"] != "active":
        raise HTTPException(status_code=400, detail="inactive user")
    new_record = {
        "record_id": record_id_counter,
        "amount": record.amount,
        "type": record.type.lower(),
        "category": record.category,
        "date": record.date,
        "description": record.description,
        "user_id": record.user_id
    }
    record_store.append(new_record)
    record_id_counter += 1
    return {"msg": "record added", "data": new_record}
@app.get("/records")
def get_records():
    return record_store
@app.post("/records")
def create_record(record: Record):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (record.user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if user["status"] != "active":
        raise HTTPException(status_code=400, detail="inactive user")
    if record.type.lower() not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="invalid type")
    cursor.execute("""
        INSERT INTO records (amount, type, category, date, description, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (record.amount, record.type.lower(), record.category, record.date, record.description, record.user_id))
    conn.commit()
    conn.close()
    return {"msg": "record saved"}
@app.get("/records")
def get_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
@app.get("/records")
@app.get("/records/filter")
def filter_records(type: str = None, category: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE 1=1"
    params = []
    if type:
        query += " AND type=?"
        params.append(type.lower())
    if category:
        query += " AND category=?"
        params.append(category)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
@app.get("/summary/income")
def total_income():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) as total FROM records WHERE type='income'")
    result = cursor.fetchone()
    conn.close()
    return {"total_income": result["total"] or 0}
@app.get("/summary/expense")
def total_expense():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) as total FROM records WHERE type='expense'")
    result = cursor.fetchone()
    conn.close()
    return {"total_expense": result["total"] or 0}
@app.get("/summary/net")
def net_balance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM records WHERE type='income'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM records WHERE type='expense'")
    expense = cursor.fetchone()[0] or 0
    conn.close()
    return {"net_balance": income - expense}
@app.get("/summary/category")
def category_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM records
        GROUP BY category
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
@app.get("/summary/recent")
def recent_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM records
        ORDER BY id DESC
        LIMIT 5
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
