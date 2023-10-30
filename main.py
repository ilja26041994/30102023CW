import psycopg2 as psycopg
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import dotenv_values


# Project:
# Name
# Lead_Name
# count_user
# is_finish
class projekt (BaseModel):
    Name: str
    Lead_Name: str
    count_user: int
    is_finish: bool


config = dotenv_values(".env")

connect = psycopg.connect(
    host=config["HOST"],
    port=config["PORT"],
    database=config["DBNAME"],
    user=config["USERID"],
    password=config["USERPW"]
)
cursor = connect.cursor()

app = FastAPI()

@app.get ('/all_projekt')
def all_projekt():
    cursor.execute("SELECT {0}, {1}, {2}, {3} FROM projekt".format("Name", "Lead_Name", "count_user", "is_finish"))
    result = cursor.fetchall()
    response = []
    for i in result:
        response.append(projekt(Name=i[0], Lead_Name=i[1], count_user=i[2], is_finish=i[3]))
    return response
