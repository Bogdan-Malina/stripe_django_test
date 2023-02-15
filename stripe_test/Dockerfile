FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "51.250.84.205:8000"]