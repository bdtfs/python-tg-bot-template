FROM python:3.13.7-slim-bookworm@sha256:adafcc17694d715c905b4c7bebd96907a1fd5cf183395f0ebc4d3428bd22d92d

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.lock ./
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.lock

RUN addgroup --system app && adduser --system --ingroup app app
COPY --chown=app:app __main__.py ./
COPY --chown=app:app app ./app
USER app

CMD ["python", "."]
