FROM python:3.10

# set workdir
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

# expose port
EXPOSE 8000

# run django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

