import uvicorn
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select

from modelos.modelos import Item,AvaliacaoItem, Vendedor, AvaliacaoVendedor
from fastapi.middleware.cors import CORSMiddleware


connect_args = {"check_same_thread": False}
engine = create_engine('sqlite://', echo=True, connect_args=connect_args, poolclass=StaticPool)

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

@app.get("/")
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()

        return items

@app.post("/items/")
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()

        return JSONResponse(content=None, status_code=201)

@app.get("/items/{item_id}")
def read_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return item

@app.patch("/items/{item_id}")
def update_item(item_id: int, item: Item):
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
def delete_items(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        session.delete(item)
        session.commit()

        return {"ok": True}
    
#endpoints avaliacao produto
#feitos os endpoints (3= get; 4= patch; 5= delete)

@app.get("/avaliacao_itens")
def read_avaliacao_itens():
    with Session(engine) as session:
        avaliacao_item = session.exec(select(AvaliacaoItem)).all()

        return avaliacao_item
    
@app.post("/avaliacao_itens")
def create_avaliacao_itens(avaliacao_itens: AvaliacaoItem):
    with Session(engine) as session:
        session.add(avaliacao_itens)
        session.commit()

        return JSONResponse(content=None, status_code=201)

@app.get("/avaliacao_itens/{avaliacao_item_id}")
def read_avaliacao_itens(avaliacao_item_id: int):
    with Session(engine) as session:
        avaliacao_item = session.get(AvaliacaoItem, avaliacao_item_id)

        if not avaliacao_item:
            raise HTTPException(status_code=404, detail="Avaliacao do Item not found")
        
        return avaliacao_item
    

@app.patch("/avaliacao_itens/{avaliacao_item_id}")
def update_avaliacao_itens(avaliacao_item_id: int, avaliacao_item: AvaliacaoItem):
    with Session(engine) as session:
        db_avaliacao_item = session.get(AvaliacaoItem, avaliacao_item_id)

        if not db_avaliacao_item:
            raise HTTPException(status_code=404, detail="Avaliacao do Item not found")
        
        avaliacao_itens_data = avaliacao_item.model_dump(exclude_unset=True)
        db_avaliacao_item.sqlmodel_update(avaliacao_itens_data)

        session.add(db_avaliacao_item)
        session.commit()
        session.refresh(db_avaliacao_item)

        return db_avaliacao_item

@app.delete("/avaliacao_itens/{avaliacao_item_id}")
def delete_avaliacao_itens(avaliacao_item_id: int):
    with Session(engine) as session:
        avaliacao_item = session.get(AvaliacaoItem, avaliacao_item_id)

        if not avaliacao_item:
            raise HTTPException(status_code=404, detail="Avaliacao do Item not found")
        
        session.delete(avaliacao_item)
        session.commit()

        return {"ok": True}


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/c/Users/Dilson/projeto-backend-mais1code")
    uvicorn.run(app, host="0.0.0.0", port=8000)