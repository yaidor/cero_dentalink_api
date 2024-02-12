FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get -y install curl

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Para desarrollo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]