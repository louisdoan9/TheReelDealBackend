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

@app.post("/get-user")
async def getUser(userInfo: User):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute('SELECT id from users where "name" = %s and pwdhash = %s', (userInfo.name, userInfo.pwdhash))

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
        cur.execute('INSERT INTO users("name", pwdhash, rname) VALUES (%s, %s, %s) RETURNING id', (userInfo.name, userInfo.pwdhash, userInfo.rname))
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

    cur.execute(f"""
    select f4.id, f4.title, count 
    from
    (
    select f, count(*)
    from
    (
    select f.fid, f2.fid as f, f.category
    from fcategory f, fcategory f2
    where f.fid <> f2.fid and f.category = f2.category and f.fid = {id}
    ) group by f order by count desc limit 2
    ), film f4
    where f4.id = f
    """                
    )
    records = cur.fetchall()

    films = []
    for film in records:
        cur.execute(f"""
        select nbc
        from normalized_film_scores nfs 
        where nfs.fid = {film[0]}
        """                
        )
        records2 = cur.fetchall()
        if len(records2) == 0: records2 = [0]

        cur.execute(f"""
        select f.category 
        from filmwithcategory f, filmwithcategory f2 
        where f.id = {film[0]} and f2.id = {id} and f.category = f2.category 
        """                
        )
        records3 = cur.fetchall()
        fixedArray = []
        for category in records3:
            fixedArray.append(category[0])
        films.append({"ID": film[0], "Title": film[1], "Matching Categories": fixedArray, "Normalized Score": records2[0]})

    

    cur.close()
    conn.close()
    return films

@app.get("/related-reviews/{id}")
async def getReviewsDetailed(id):
    conn = psycopg2.connect(f"dbname=TheReelDealDB user=TheReelDealDB_owner password={os.getenv('DBPASSWORD')} port=5432 host=ep-tight-mode-a53mncek.us-east-2.aws.neon.tech")
    cur = conn.cursor()

    cur.execute(f"""
    select a.id, a.title, a.rtime, count 
    from article a,
    (
    select f, count(*)
    from
    (
    select f.aid, f2.aid as f, f.fid
    from fmention f, fmention f2 
    where f.aid <> f2.aid and f.fid = f2.fid and f.aid = {id}
    ) group by f order by count desc limit 2)
    where a.id = f
    order by count desc
    """                
    )
    records = cur.fetchall()
    print(records)

    reviews = []
    for review in records:
        cur.execute(f"""
        select r."Film title" 
        from reviewwithfilm r, reviewwithfilm r2 
        where r."Review ID" = {review[0]} and r2."Review ID" = {id} and r."Film ID"  = r2."Film ID" 
        """                
        )
        records2 = cur.fetchall()
        fixedArray = []
        for film in records2:
            fixedArray.append(film[0])
        reviews.append({"ID": review[0], "Title": review[1], "Date": review[2], "Matching Films": fixedArray})

    

    cur.close()
    conn.close()
    return reviews