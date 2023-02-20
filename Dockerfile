# Dockerfile-flask

# Simply inherit the Python 3 image.
FROM python:3.8

RUN apt update
RUN apt install -y nginx supervisor
RUN pip3 install gunicorn

# Set an environment variable
ENV APP /app

# Create the directory
RUN mkdir $APP
WORKDIR $APP


# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx_flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx_flask.conf /etc/nginx/sites-enabled/nginx_flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf


# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/bin/bash"]
# Finally, we run uWSGI with the ini file