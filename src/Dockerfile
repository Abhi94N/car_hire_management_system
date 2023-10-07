FROM python:3.9.18-alpine3.18

ENV PORT 5000
ENV HOST 0.0.0.0
ENV FLASK_DEBUG 0

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE $PORT 
CMD if [ "$FLASK_DEBUG" = "1" ]; then \
        export FLASK_APP=app.py FLASK_ENV=development FLASK_RUN_HOST=$HOST FLASK_RUN_PORT=$PORT && flask run; \
    else \
        gunicorn -b $HOST:$PORT -w 4 app:app; \
    fi