# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends

# Add Google's public key
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Set up the Chrome repository
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list

# Install Chrome
RUN apt-get update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN apt-get install -y chromium-driver

# Install chromedriver_autoinstaller
RUN pip install chromedriver-autoinstaller

# Clean up APT when done
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Define environment variable
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Copy the rest of the application code into the container
COPY . .

# Run flask when the container launches
CMD ["flask", "run", "--port=8081"]
