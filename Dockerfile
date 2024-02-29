FROM python:3.12.1-slim-bullseye
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "./services/products.py"]