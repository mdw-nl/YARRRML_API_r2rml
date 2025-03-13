# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
# Prevents Python from writing pyc files to disc (also helps in debugging!)
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr (also helps in debugging!)
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc g++ libyaml-dev \
 && apt-get install -y --no-install-recommends curl gnupg \
 && apt-get install -y libpq-dev

# Install Node.js LTS and npm
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
 && apt-get install -y nodejs

RUN node -v
RUN npm -v

RUN npm i -g @rmlio/yarrrml-parser

# Copy the local requirements file to the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local code to the container
COPY testyarml/ /app/

# Specify the command to run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]