from fastapi import FastAPI, Depends
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import schemas

app = FastAPI()
Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


fake_database = {
    1: {'task': 'Clean car'},
    2: {'task': 'Write blog'},
    3: {'task': 'Start stream'},
    4: {'task': 'Nothing todo'},
}


@app.get("/")
def get_items(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get('/{id}')
def get_items(id: int):
    return fake_database[id]


@app.post("/")
def add_items(item: schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.put("/{id}")
def update_item(id: int, item: schemas.Item):
    fake_database[id]['task'] = item.task
    return fake_database


@app.delete("/{id}")
def delete_item(id: int):
    del fake_database[id]
    return fake_database
