FROM alpine:latest

# pull official base image
FROM python:3.7.3-slim

# set work directory
WORKDIR /app

COPY . /app

# Set up Virtual Environment
# ENV VIRTUAL_ENV "/budgetenv"
# RUN python -m venv $VIRTUAL_ENV
# ENV PATH "$VIRTUAL_ENV/bin:$PATH"
ENV PATH=$PATH:/app/.local/bin



# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=budgetapi
ENV FLASK_ENV=development

RUN export FLASK_APP
RUN export FLASK_ENV


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /flaskapi/requirements.txt
RUN pip install -r requirements.txt

# initialize db
RUN flask db init
RUN flask db migrate -m "Initial migration."
RUN flask db upgrade

# copy project
COPY . /app/

# run entrypoint.sh
# ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 5000


# ENTRYPOINT [ "python" ]
# CMD [ "budgetapi.py" ]

CMD ["flask", "run", "--host", "0.0.0.0"]
