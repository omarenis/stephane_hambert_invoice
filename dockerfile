FROM ubuntu:18.04
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install build-essential manpages-dev apt-utils tar make
RUN apt-get install -y software-properties-common
RUN apt install -y wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
RUN wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
RUN tar -xf Python-3.8.0.tgz
RUN cd Python-3.8.0 && ./configure --enable-optimizations && make -j 8 && make altinstall && cd ../
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
RUN apt install -y ./wkhtmltox_0.12.6-1.bionic_amd64.deb
RUN mkdir app && cd app
WORKDIR app
COPY . .
RUN python3.8 -m pip install -r requirements.txt
ENTRYPOINT FLASK_APP=/home/app.py flask run --host=0.0.0.0

