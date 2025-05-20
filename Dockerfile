FROM python:3.12-slim

# Consider removing when running in production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py db.py tests.py tests.sh ./

EXPOSE 5001

# Run the app
CMD ["python", "app.py"]