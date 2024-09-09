# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:slim-bullseye   

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN apt-get update 
RUN apt-get --yes --force-yes install libpq-dev libpq-dev python3-dev gcc
RUN pip install -U pip
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app



# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "aina.py"]
