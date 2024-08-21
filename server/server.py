import uvicorn
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select

from modelos.modelos import Item,Vendedor, AvaliacaoVendedor
from fastapi.middleware.cors import CORSMiddleware


connect_args = {"check_same_thread": False}
engine = create_engine('sqlite:///file1.db', echo=True, connect_args=connect_args, poolclass=StaticPool)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

# Observe que CORS apenas eh retornado quando os Headers do requerimento GET incluem "Origin".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
	allow_headers=["*"],
    max_age=3600,
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/items/")
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()

        return JSONResponse(content=None, status_code=201)

@app.get("/")
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()

        return items
    
@app.get("/items/{item_id}")
def read_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return item

@app.patch("/items/{item_id}")
def update_hero(item_id: int, item: Item):
    with Session(engine) as session:
        db_item = session.get(Item, item_id)

        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        item_data = item.model_dump(exclude_unset=True)
        db_item.sqlmodel_update(item_data)

        session.add(db_item)
        session.commit()
        session.refresh(db_item)

        return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        session.delete(item)
        session.commit()

        return {"ok": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)