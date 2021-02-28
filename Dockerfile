FROM python:3

RUN mkdir -p /app/src

WORKDIR /app/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]