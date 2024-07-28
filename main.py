from fastapi import FastAPI
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/article")
async def root():
    conn = psycopg2.connect("dbname=TheReelDealDB user=TheReelDealDB_owner password=dLjDYV12qhCp port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()
    cur.execute("SELECT * FROM article")
    records = cur.fetchall()
    cur.close()
    conn.close()
    return records