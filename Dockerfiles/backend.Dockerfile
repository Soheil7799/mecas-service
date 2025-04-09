FROM python:3.13.2-slim-bookworm

WORKDIR /app

RUN apt update && \
    apt install -y ffmpeg

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ../. .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]