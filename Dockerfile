FROM python:3.13.0-alpine

WORKDIR /app

ENV DISCORD_TOKEN=""
ENV REPLICATE_API_TOKEN=""
ENV RASA_URL=""

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY bot.py .

CMD ["python3", "-m", "bot.py"]