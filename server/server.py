import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from modelos.modelos import Item, AvaliacaoItem, LikesAvaliacaoItem, \
    AvaliacaoItemPublic

connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///database.db", echo=True, connect_args=connect_args, poolclass=StaticPool)

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

@app.get("/avaliacao_itens/{avaliacao_item_id}", response_model=AvaliacaoItemPublic)
def read_avaliacao_itens(avaliacao_item_id: int):
    with Session(engine) as session:
        avaliacao_item = session.get(AvaliacaoItem, avaliacao_item_id)

        if not avaliacao_item:
            raise HTTPException(status_code=404, detail="Avaliacao do Item not found")
        
        print (avaliacao_item.likes)
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
    
@app.post("/likes_avaliacao_items/")
def create_likes_avaliacao_items(likes_avaliacao_items: LikesAvaliacaoItem):
    with Session(engine) as session:
        session.add(likes_avaliacao_items)
        session.commit()

        return JSONResponse(content=None, status_code=201)

@app.get("/likes_avaliacao_items/{likes_avaliacao_items_id}")
def read_likes_avaliacao_items(likes_avaliacao_items_id: int):
    with Session(engine) as session:
        likes_avaliacao_items = session.get(Item, likes_avaliacao_items_id)

        if not likes_avaliacao_items:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return likes_avaliacao_items

@app.patch("/likes_avaliacao_items/{likes_avaliacao_items_id}")
def update_likes_avaliacao_items(likes_avaliacao_items_id: int, likes_avaliacao_items: LikesAvaliacaoItem):
    with Session(engine) as session:
        db_likes_avaliacao_items = session.get(LikesAvaliacaoItem, likes_avaliacao_items_id)

        if not db_likes_avaliacao_items:
            raise HTTPException(status_code=404, detail="Likes not found")
        
        likes_avaliacao_items_data = likes_avaliacao_items.model_dump(exclude_unset=True)
        db_likes_avaliacao_items.sqlmodel_update(likes_avaliacao_items_data)

        session.add(db_likes_avaliacao_items)
        session.commit()
        session.refresh(db_likes_avaliacao_items)

        return db_likes_avaliacao_items

@app.delete("/likes_avaliacao_items/{likes_avaliacao_items_id}")
def delete_likes_avaliacao_items(likes_avaliacao_items_id: int):
    with Session(engine) as session:
        likes_avaliacao_items = session.get(LikesAvaliacaoItem, likes_avaliacao_items_id)

        if not likes_avaliacao_items:
            raise HTTPException(status_code=404, detail="Likes not found")
        
        session.delete(likes_avaliacao_items)
        session.commit()

        return {"ok": True}



if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/c/Users/Dilson/projeto-backend-mais1code")
    uvicorn.run(app, host="0.0.0.0", port=8000)