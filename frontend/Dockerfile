FROM node:8.12.0

LABEL author="Benny Hwang"

WORKDIR /frontend
COPY . frontend/

WORKDIR frontend

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]