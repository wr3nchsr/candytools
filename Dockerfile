FROM python:3-slim-buster

WORKDIR /root/
ADD . /root/

RUN apt update
RUN apt -y install make g++ zlib1g-dev curl git p7zip-full cpio openjdk-11-jre file

RUN chmod +x ./install.sh
RUN ./install.sh

ENTRYPOINT ["python3", "./candy.py"]
CMD ["--help"]