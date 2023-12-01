FROM python:latest
WORKDIR /highlight-extractor
COPY . /highlight-extractor/
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update
RUN apt install -y default-jdk

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN mkdir /root/.conda
RUN bash Miniconda3-latest-Linux-x86_64.sh -b

RUN conda install --yes -c conda-forge gcc 
RUN conda install --yes -c conda-forge jpype1

RUN pip install -r requirements.txt

EXPOSE 10000
ENTRYPOINT ["gunicorn", "api:app", "-b", ":10000", "--timeout", "0"]