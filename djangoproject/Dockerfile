#erlier: python:3.13-alpine
FROM python:3.13-slim
#try multistage later
WORKDIR /djangoproject
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /djangoproject/

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]