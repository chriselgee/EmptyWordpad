FROM python:3.10.8-buster
LABEL maintainer="christopher.elgee@gmail.com"

ENV PORT=$PORT

WORKDIR /app
# next lines aren't most efficient for prod, but doing things in this order makes rebuilding the Docker image faster when there are changes to the app
COPY ./app/requirements.txt /app
RUN python3 -m pip install -r requirements.txt --upgrade
RUN python3 -m pip install gunicorn

COPY ./app /app

# CMD ["/bin/bash"] # for severe debugging only
# ENTRYPOINT [ "python" ]
# CMD ["gunicorn","-b","0.0.0.0:${PORT}","main:app" ]
CMD exec gunicorn -b 0.0.0.0:$PORT main:app