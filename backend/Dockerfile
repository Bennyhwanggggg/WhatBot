FROM python:3.7

LABEL author="Benny Hwang"

RUN apt-get update && apt-get install -y \
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

CMD ["python3", "./app.py"]