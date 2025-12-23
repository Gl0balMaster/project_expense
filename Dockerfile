FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN useradd -m -u 1000 user && chown -R user:user /app
USER user

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]