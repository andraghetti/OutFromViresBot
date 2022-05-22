FROM python:3.9-slim

RUN mkdir /bot
COPY --chmod=755 ./*.py /bot
WORKDIR /bot

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir . --target /bot

CMD [ "python", "bot.py" ]
