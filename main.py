from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

# .env variables
import os
from dotenv import load_dotenv
load_dotenv()

class User(BaseModel):
    name: str
    pwdhash: str
    rname: Optional[str] = None

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

@app.get("/reviews-partial")
async def getReviewsPartial():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()
    partialReviews = []

    cur.execute('select * from reviewwithauthor order by "Review date" DESC')
    reviews = cur.fetchall()

    for review in reviews:
        cur.execute('select * from getreviewfilms(%s)', (review[0],))
        reviewFilms = cur.fetchall()

        mentionedFilms = []
        for film in reviewFilms:
            mentionedFilms.append({"ID": film[0], "Title": film[1]})

        partialReview = {"ID": review[0], "Title": review[1], "Date": review[3], "Author": review[4], "Mentioned Films": mentionedFilms}
        partialReviews.append(partialReview)

    cur.close()
    conn.close()
    return partialReviews

@app.get("/reviews-partial/latest")
async def getReviewsPartial():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()
    partialReviews = []

    cur.execute('select * from reviewwithauthor order by "Review date" DESC LIMIT 8')
    reviews = cur.fetchall()

    for review in reviews:
        cur.execute('select * from getreviewfilms(%s)', (review[0],))
        reviewFilms = cur.fetchall()

        mentionedFilms = []
        for film in reviewFilms:
            mentionedFilms.append({"ID": film[0], "Title": film[1]})

        partialReview = {"ID": review[0], "Title": review[1], "Date": review[3], "Author": review[4], "Mentioned Films": mentionedFilms}
        partialReviews.append(partialReview)

    cur.close()
    conn.close()
    return partialReviews

@app.get("/reviews-detailed/{id}")
async def getReviewsDetailed(id):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute('select * from getreviewauthors(%s)', (id,))
    reviews = cur.fetchall()

    detailedReview = {}
    for review in reviews:
        cur.execute('select * from getreviewfilms(%s)', (review[0],))
        reviewFilms = cur.fetchall()
        
        mentionedFilms = []
        for film in reviewFilms:
            mentionedFilms.append({"ID": film[0], "Title": film[1], "Score": film[2]})

        detailedReview = {"ID": review[0], "Title": review[1], "Body": review[2], "Date": review[3], "Author": review[4], "Mentioned Films": mentionedFilms}


    cur.close()
    conn.close()
    return detailedReview

@app.get("/films-partial")
async def getReviewsPartial():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute("select * from getpartialfilms()")
    films = cur.fetchall()

    partialFilms = []
    for film in films:
        partialFilms.append({"ID": film[0], "Title": film[1], "Normalized Score": film[2]})

    cur.close()
    conn.close()
    return partialFilms

@app.get("/films-partial/top")
async def getReviewsPartial():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute("select * from getpartialfilms() LIMIT 3")
    films = cur.fetchall()

    partialFilms = []
    for film in films:
        partialFilms.append({"ID": film[0], "Title": film[1], "Normalized Score": film[2]})

    cur.close()
    conn.close()
    return partialFilms


@app.get("/films-detailed/{id}")
async def getReviewsDetailed(id):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute('select * from getdetailedfilm(%s)', (id,))
    film = cur.fetchall()[0]
        
    cur.execute('select * from getfilmcategories(%s)', (id,))
    filmCategories = cur.fetchall()

    includedCategories = []
    for category in filmCategories:
        includedCategories.append(category[0])
    
    detailedFilm = {"ID": film[0], "Title": film[1], "Normalized Score": film[2], "Score Trend": film[3], "Film Categories": includedCategories}

    cur.close()
    conn.close()
    return detailedFilm

@app.post("/get-user")
async def getUser(userInfo: User):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute("select * from getuser(%s, %s)", (userInfo.name, userInfo.pwdhash))

    records = cur.fetchall()

    cur.close()
    conn.close()
    if (len(records) > 0):
        return {"userInfo": records[0]}
    else:
        return {"message": "User not found"}

@app.post("/create-user")
async def createUser(userInfo: User):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    try:
        cur.execute('select * from createuser(%s, %s, %s)', (userInfo.name, userInfo.pwdhash, userInfo.rname))
        conn.commit()
        
        records = cur.fetchall()

        cur.close()
        conn.close()
        return {"userInfo": records[0]}
    except:
        return {"message": "failed"}
    

@app.get("/related-films/{id}")
async def getReviewsDetailed(id):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute("select * from getrelatedfilms(%s)", (id,))
    films = cur.fetchall()

    relatedFilms = []
    for film in films:
        cur.execute("select * from getpartialfilm(%s)", (film[0],))
        partialfilm = cur.fetchall()

        cur.execute("select * from getsharedcategories(%s, %s)", (id, film[0]))
        categories = cur.fetchall()

        sharedCategories = []
        for category in categories:
            sharedCategories.append(category[0])

        relatedFilms.append({"ID": partialfilm[0][0], "Title": partialfilm[0][1], "Matching Categories": sharedCategories, "Normalized Score": partialfilm[0][2]})

    cur.close()
    conn.close()
    return relatedFilms

@app.get("/related-reviews/{id}")
async def getReviewsDetailed(id):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute(f"select * from getrelatedreviews({id})")
    reviews = cur.fetchall()

    relatedReviews = []
    for review in reviews:
        cur.execute(f"select * from getreviewauthors({review[0]})")
        partialReview = cur.fetchall()

        cur.execute(f"select * from getsharedfilms({id}, {review[0]})")
        films = cur.fetchall()

        sharedFilms = []
        for film in films:
            sharedFilms.append(film[0])
            
        relatedReviews.append({"ID": partialReview[0][0], "Title": partialReview[0][1], "Author": partialReview[0][4], "Date": partialReview[0][3], "Matching Films": sharedFilms})

    cur.close()
    conn.close()
    return relatedReviews