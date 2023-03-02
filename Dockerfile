FROM --platform=linux/amd64 python:3.8

RUN apt-get update -y

COPY requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN pip install -r requirements.txt

COPY . /opt/app

RUN pip install -e .

CMD ["python3", "chatgpt_bot/bot.py"]
