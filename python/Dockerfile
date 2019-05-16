# Dockerfile for the DemocracyWorks Python environment.
FROM python:3.7.3-alpine3.8

ARG WORKDIR=.
WORKDIR $WORKDIR

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=elections
ENV FLASK_ENV=development

EXPOSE 5000/tcp

# Expose Flask on "all" interfaces because we are inside a container.
CMD [ "flask", "run", "--host", "0.0.0.0" ]
