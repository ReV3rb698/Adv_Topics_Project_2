FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5003
CMD ["python", "server.py"]
