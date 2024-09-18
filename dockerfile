# Use an official Node.js runtime as a parent image
FROM python:3.10.12

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

RUN python manage.py makemigrations backend

RUN python manage.py migrate

RUN cd frontend && npm install && npm run dev

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]