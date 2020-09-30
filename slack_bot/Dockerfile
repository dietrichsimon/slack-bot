# Use an official Python runtime as a parent image
FROM python:3.7.7-slim

# set the working directory to /app
# inside the container
WORKDIR /app

# copy the requirements file into the container at /app
# (a text file with all the libraries you want to install)
# (like scp command to transfer files to EC2 machine)
ADD requirements.txt /app

ADD bot.py /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run bot.py when the container launches
CMD ["python", "bot.py"]
