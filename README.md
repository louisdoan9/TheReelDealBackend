# The Reel Deal (backend) 🎬

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

Backend for The Reel Deal. Fetches information from the PostgreSQL database. Retrieves information from the database when requested from the frontend.

## Deployment 🚀

https://the-reel-deal-backend.vercel.app/

## API Reference 🧩

#### Get partial review data for all reviews

```http
  GET /reviews-partial
```

#### Get partial review data for latest reviews

```http
  GET /reviews-partial/latest
```

#### Get detailed review data for a review with {id}

```http
  GET /reviews-detailed/{id}
```

#### Get partial film data for all films

```http
  GET /films-partial
```

#### Get partial film data for top films

```http
  GET /films-partial/top
```

#### Get detailed film data for a film with {id}

```http
  GET /films-detailed/{id}
```

#### Get user with corresponding username and password

```http
  POST /get-user
```

#### Create user with corresponding username, password, and real name

```http
  POST /create-user
```

#### Get related films for a film with {id}

```http
  GET /related-films/{id}
```

#### Get related reviews for a review with {id}

```http
  GET /related-reviews/{id}
```

## Related

- [The Reel Deal Frontend](https://github.com/louisdoan9/TheReelDeal)
