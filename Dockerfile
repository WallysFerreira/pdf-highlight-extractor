FROM python:latest
WORKDIR /highlight-extractor
COPY . /highlight-extractor/

RUN apt-get update
RUN apt-get -y install tesseract-ocr-por poppler-utils
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["gunicorn", "api:app", "--timeout", "0"]