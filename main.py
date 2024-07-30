from fastapi import FastAPI
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

# .env variables
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# fixes CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TheReelDealBackend"}

@app.get("/article")
async def article():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()
    cur.execute("SELECT * FROM article")
    records = cur.fetchall()
    cur.close()
    conn.close()
    return records

@app.get("/article/latest")
async def article():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()
    cur.execute("select * from article order by rtime desc limit 8")
    records = cur.fetchall()
    cur.close()
    conn.close()
    return records

@app.get("/reviews-detailed")
async def article():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute("select * from reviewwithauthor")
    records1 = cur.fetchall()

    cur.execute("select * from reviewwithfilm")
    records2 = cur.fetchall()

    cur.execute("select * from filmwithcategory")
    records3 = cur.fetchall()

    reviews = []
    for reviewDetails in records1:
        mentionedFilms = []

        for reviewFilms in records2:
            if  reviewDetails[0] == reviewFilms[0]:
                filmCategories = []
                for reviewCategories in records3:
                    if reviewCategories[0] == reviewFilms[1]:
                        filmCategories.append(reviewCategories[1])
                mentionedFilms.append({"ID": reviewFilms[1], "Title": reviewFilms[2], "Score": reviewFilms[3], "Categories": filmCategories})

        review = {"ID": reviewDetails[0], "Title": reviewDetails[1], "Body": reviewDetails[2], "Date": reviewDetails[3], "Author": reviewDetails[4], "Mentioned Films": mentionedFilms}
        reviews.append(review)


    cur.close()
    conn.close()
    return reviews

@app.get("/reviews-detailed/{id}")
async def article(id):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute("select * from reviewwithauthor")
    records1 = cur.fetchall()

    cur.execute("select * from reviewwithfilm")
    records2 = cur.fetchall()

    cur.execute("select * from filmwithcategory")
    records3 = cur.fetchall()

    reviews = []
    for reviewDetails in records1:
        mentionedFilms = []

        for reviewFilms in records2:
            if  reviewDetails[0] == reviewFilms[0]:
                filmCategories = []
                for reviewCategories in records3:
                    if reviewCategories[0] == reviewFilms[1]:
                        filmCategories.append(reviewCategories[1])
                mentionedFilms.append({"ID": reviewFilms[1], "Title": reviewFilms[2], "Score": reviewFilms[3], "Categories": filmCategories})

        review = {"ID": reviewDetails[0], "Title": reviewDetails[1], "Body": reviewDetails[2], "Date": reviewDetails[3], "Author": reviewDetails[4], "Mentioned Films": mentionedFilms}
        reviews.append(review)


    cur.close()
    conn.close()
    return reviews[int(id)]