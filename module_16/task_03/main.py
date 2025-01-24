from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Examples, возраст: 18'}

@app.get("/users")
async def get_users() -> dict:
    return users

@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(title="Enter username", description="Enter username", min_length=5, max_length=20, examples={'default': {'summary': 'Standard username', 'value': 'UrbanUser'}})],
                      age: Annotated[int, Path(title="Enter age", description="Enter age", ge=18, le=120, examples={'default': {'summary': 'Standard age', 'value': 24}})]) -> str:
    user_id = str(max(int(key) for key in users.keys()) + 1)
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(title="Enter User ID", description="Enter User ID", ge=1, le=100, examples={'default': {'summary': 'Example user ID', 'value': 1}})],
                      username: Annotated[str, Path(title="Enter username", description="Enter username", min_length=5, max_length=20, examples={'default': {'summary': 'Example username', 'value': 'UrbanProfi'}})],
                      age: Annotated[int, Path(title="Enter age", description="Enter age", ge=18, le=120, examples={'default': {'summary': 'Example age', 'value': 28}})]) -> str:
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str] = f"Имя: {username}, возраст: {age}"
        return f"User {user_id_str} has been updated"
    else:
        return f"User {user_id_str} not found"

@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(title="Enter User ID", description="Enter User ID", ge=1, le=100, examples={'default': {'summary': 'Example user ID', 'value': 2}})]) -> str:
    user_id_str = str(user_id)
    if user_id_str in users:
        del users[user_id_str]
        return f"User {user_id_str} has been deleted"
    else:
        return f"User {user_id_str} not found"