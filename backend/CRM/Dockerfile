FROM python:3.13

WORKDIR /app
COPY . /app

RUN python3 -m venv venv
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt

EXPOSE 8100
CMD ["./venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"]
