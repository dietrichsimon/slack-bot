# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
# inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
# (a text files with all the libraries you want to install)
# (like scp)
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
# inside the container
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the .py file into docker
COPY etl.py /app

# Run hello.py when the container launches
CMD ["python", "etl.py"]
