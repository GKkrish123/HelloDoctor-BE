# DOCKER FASTAPI IMAGE
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# PORT FORWARD -> Default 5000
ENV PORT=5000
EXPOSE 5000

# POINT STARTUP ENV
ENV MODULE_NAME app.startup

# INSTALL REQUIREMENTS
COPY ./requirements.txt /hellodoctor/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /hellodoctor/requirements.txt

# CHANGE WORK DIRECTORY
COPY . /hellodoctor
WORKDIR /hellodoctor