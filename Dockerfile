FROM alpine:3.12

RUN apk add --update ca-certificates python3 py3-pip py3-setuptools py3-wheel curl

RUN adduser -s /bin/bash -D -u 1000 -h /srv/app app && \
  mkdir -p /srv/app && \
  chown -R app.app /srv/app
USER app
WORKDIR /srv/app

ADD --chown=1000:1000 . /srv/app/
RUN pip3 install --user --no-cache-dir -r /srv/app/requirements/runtime.txt


ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:/srv/app
ENV PATH=$PATH:/srv/app/.local/bin
ARG VERSION=0.0.0-notset
ENV ENVIRONMENT=production
ENV COLOR=gray

RUN /bin/sh -c 'echo "VERSION='"$VERSION"'" > /srv/app/version.env'

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s \
  CMD curl -f http://127.0.0.1:8000/healthcheck || exit 1

ENTRYPOINT ["/srv/app/docker-entrypoint.sh"]
CMD ["run"]
