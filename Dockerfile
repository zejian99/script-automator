# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Create the data directory
RUN mkdir /app/data

# Copy the script and configuration files into the container
COPY generate_summary.py config.py requirements.txt .env /app/

RUN apt-get update && apt-get install -y libnotify-bin && apt-get install -y libssl-dev

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the display environment variable for GUI notifications (optional)
ENV DISPLAY=:0

# Run the script when the container starts
CMD ["python", "generate_summary.py"]
