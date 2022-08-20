from fastapi import FastAPI

import schemas

app = FastAPI()

fake_database = {
    1: {'task': 'Clean car'},
    2: {'task': 'Write blog'},
    3: {'task': 'Start stream'},
    4: {'task': 'Nothing todo'},
}


@app.get("/")
def get_items():
    return fake_database


@app.get('/{id}')
def get_items(id: int):
    return fake_database[id]


@app.post("/")
def add_items(item: schemas.Item):
    new_id = len(fake_database.keys()) + 1
    fake_database[new_id] = {"task": item.task}
    return fake_database


@app.put("/{id}")
def update_item(id: int, item: schemas.Item):
    fake_database[id]['task'] = item.task
    return fake_database


@app.delete("/{id}")
def delete_item(id: int):
    del fake_database[id]
    return fake_database
