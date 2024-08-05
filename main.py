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

    cur.execute('select * from reviewwithauthor order by "Review date" DESC')
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
                mentionedFilms.append({"ID": reviewFilms[1], "Title": reviewFilms[2]})

        review = {"ID": reviewDetails[0], "Title": reviewDetails[1], "Date": reviewDetails[3], "Author": reviewDetails[4], "Mentioned Films": mentionedFilms}
        reviews.append(review)


    cur.close()
    conn.close()
    return reviews

@app.get("/reviews-partial/latest")
async def getReviewsPartialLatest():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute('select * from reviewwithauthor order by "Review date" DESC LIMIT 8')
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
                mentionedFilms.append({"ID": reviewFilms[1], "Title": reviewFilms[2]})

        review = {"ID": reviewDetails[0], "Title": reviewDetails[1], "Date": reviewDetails[3], "Author": reviewDetails[4], "Mentioned Films": mentionedFilms}
        reviews.append(review)


    cur.close()
    conn.close()
    return reviews

@app.get("/reviews-detailed/{id}")
async def getReviewsDetailed(id):
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
    return next((review for review in reviews if review["ID"] == int(id)), None)

@app.get("/films-partial")
async def getReviewsPartial():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute("""
    select id, title, nfs.nbc 
    from film f, normalized_film_scores nfs 
    where f.id = nfs.fid 
    order by nbc DESC
    """                
    )
    records1 = cur.fetchall()

   
    cur.execute(f"""
    select id, title, 0 as nbc
    from film f
    where f.id NOT in (
        select id
        from film f, normalized_film_scores nfs 
        where f.id = nfs.fid 
        order by nbc DESC
    )
    """                
    )
    records2 = cur.fetchall()

    cur.close()
    conn.close()
    return records1 + records2

@app.get("/films-partial/latest")
async def getReviewsPartial():
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute("""
    select id, title, nfs.nbc
    from film f, normalized_film_scores nfs 
    where f.id = nfs.fid 
    order by nbc DESC LIMIT 3
    """                
    )
    records = cur.fetchall()

    cur.close()
    conn.close()
    return records


@app.get("/films-detailed/{id}")
async def getReviewsDetailed(id):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute(f"""
    select id, title, nfs.nbc, fst.ts 
    from film f, normalized_film_scores nfs, film_scoring_trends fst 
    where f.id = nfs.fid and fst.fid = nfs.fid and f.id = {id}
    order by nbc DESC
    """                
    )
    records1 = cur.fetchall()

    noNormalized = False
    if (records1 == []):
        cur.execute(f"""
        select id, title, fst.ts 
        from film f, film_scoring_trends fst 
        where f.id = fst.fid and f.id = {id}
        """                
        )
        records1 = cur.fetchall()
        noNormalized = True

    cur.execute("select * from filmwithcategory")
    records2 = cur.fetchall()

    films = []
    for film in records1:
        filmCategories = []
        for category in records2:
            if category[0] == film[0]:
                filmCategories.append(category[1])
        if noNormalized: films.append({"ID": film[0], "Title": film[1], "Normalized Score": 0, "Score Trend": film[2], "Film Categories": filmCategories})
        else : films.append({"ID": film[0], "Title": film[1], "Normalized Score": film[2], "Score Trend": film[3], "Film Categories": filmCategories})


    cur.close()
    conn.close()
    return next((film for film in films if film["ID"] == int(id)), None)

@app.post("/users")
async def getReviewsDetailed(userInfo: User):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute('INSERT INTO users("name", pwdhash, rname) VALUES (%s, %s, %s)', (userInfo.name, userInfo.pwdhash, userInfo.rname))

    conn.commit()

    cur.close()
    conn.close()
    return {"message": "success"}