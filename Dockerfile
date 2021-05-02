FROM python:3.8

RUN apt-get update && apt-get upgrade -y && apt install -y tesseract-ocr

WORKDIR /usr/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FRAMES_DIR=/usr/app/frames

CMD [ "python", "cli.py" ]
