FROM python:3

COPY world_capitals_bot/ /app
COPY conversation_module/ /app
COPY game_module /app

WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]



