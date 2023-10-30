from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2 as psycopg
from dotenv import dotenv_values
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
from urllib import request

# Project:
# Name
# Lead_Name
# count_user
# is_finish
# Для созданного проекта добавить endpoins:
# 1. Чтение записи по ID
# 2. Добавление записи
# 3. Удаление записи по ID

app = FastAPI()

config = dotenv_values(".env")

connection = connect(
    dbname=config["POSTGRES_DB"],
    user=config["POSTGRES_USER"],
    password=config["POSTGRES_PASSWORD"],
    host=config["POSTGRES_HOST"],
    port=config["POSTGRES_PORT"]
)

cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    lead_name VARCHAR(255),
    count_user INT,
    is_finish BOOLEAN
)
""")


# cursor.execute("""insert into projects (name, lead_name, count_user, is_finish) values
# ('test', 'test', 1, false),
# ('test2', 'test2', 2, false),
# ('test3', 'test3', 3, false),
# ('test4', 'test4', 4, false),
# ('test5', 'test5', 5, false),
# ('test6', 'test6', 6, false),
# ('test7', 'test7', 7, false),
# ('test8', 'test8', 8, false),
# ('test9', 'test9', 9, false),
# ('test10', 'test10', 10, false)
#     """)




class Project(BaseModel):
    name: str
    lead_name: str
    count_user: int
    is_finish: bool



@app.get("/project/id")
def get_project(id):
    cursor.execute(f"SELECT * FROM projects WHERE id = {id}")
    reslist = []
    for i in cursor.fetchall():
        reslist.append({"id": i[0], "name": i[1], "lead_name": i[2], "count_user": i[3], "is_finish": i[4]})
    return reslist

@app.put("/project/id")
def update_project(id):
    name = request.json.get("name")
    lead_name = request.json.get("lead_name")
    count_user = request.json.get("count_user")
    is_finish = request.json.get("is_finish")
    cursor.execute(f"UPDATE projects SET name = '{name}', lead_name = '{lead_name}', count_user = {count_user}, is_finish = {is_finish} WHERE id = {id}")
    return "ok"

@app.delete("/project/id")
def delete_project(id):
    cursor.execute(f"DELETE FROM projects WHERE id = {id}")
    return "ok"

# Подключение к БД
connection.commit()

# Подключение к БД
connection.close()


