FROM python:3.7

LABEL author="Benny Hwang"

RUN apt-get update && apt-get install -y \
    nginx \
    build-essential \
	python \
	python-pip \
	&& rm -rf /var/lib/apt/lists/*	
RUN pip install --upgrade pip

WORKDIR /backend
COPY . backend/

WORKDIR backend

RUN pip install -r requirements.txt
RUN python3 setup.py install
RUN chmod +x ./start_tests.sh 

EXPOSE 9999

COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]