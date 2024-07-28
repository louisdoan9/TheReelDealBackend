FROM python

WORKDIR /app

RUN pip install fastapi

RUN pip install psycopg2-binary

COPY . .

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]