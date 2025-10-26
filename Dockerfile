# Step 1: Set the base image to Python 3.9
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt to the container and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Step 4: Copy the entire application to the container
COPY . /app

# Step 5: Expose the port that Flask runs on (default is 5000)
EXPOSE 5000

# Step 6: Set the environment variable for Flask (optional, for production use)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Step 7: Set the command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
