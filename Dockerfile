# Use Ubuntu as base image
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Thunderbird and required dependencies
RUN apt-get update && apt-get install -y \
    thunderbird \
    dbus-x11 \
    x11-utils \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install necessary Python libraries
# RUN pip3 install smtplib email

# Copy the Python script into the container
COPY send_email.py /root/send_email.py

# Set the working directory
WORKDIR /root

# Command to run the Python script (for now, it will be an empty placeholder)
CMD ["python3", "send_email.py"]
