# Use official Python base image
FROM python:3.10-slim

# set workdir
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# expose Django default port
EXPOSE 8000

# start Django app with python3 and -p flag
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "-p", "8000"]

