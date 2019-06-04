# We Use an official Python runtime as a parent image
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /mum_food

WORKDIR /mum_food

# Copy the current directory contents into the container at
ADD . /mum_food/
COPY requirements.txt /code/
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
