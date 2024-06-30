# Set base image (host os)
FROM python:3.12-slim

# By default, listen on port seee
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire content of the local project directory to the working directory
COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]