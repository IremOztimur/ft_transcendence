# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /tournament-app

COPY . /tournament-app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /tournament-app/requirements.txt

# Expose the port that the Django app runs on
EXPOSE 8000

CMD [ "bash", "./tools/microservice-run.sh" ]
