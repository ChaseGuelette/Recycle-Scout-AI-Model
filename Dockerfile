# Set base image (host os)
FROM python:3.8-slim

# By default, listen on port seee
#EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the entire content of the local project directory to the working directory
COPY . .

ENV FLASK_APP=app.py

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]