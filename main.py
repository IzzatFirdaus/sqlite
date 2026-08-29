from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 1. Define SQLModel / Database Schema
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    price: float
    is_available: bool = True

# 2. Configure SQLite Engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# 3. Helper to initialize database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 4. Dependency to handle database sessions per request
def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(title="FastAPI + SQLite Persistence API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Endpoint: Create Item in SQLite DB
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

# Endpoint: Get All Items from SQLite DB
@app.get("/items/", response_model=List[Item])
def read_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items

# Endpoint: Get Single Item by ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Endpoint: Delete Item from DB
@app.delete("/items/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"message": f"Item {item_id} deleted successfully"}