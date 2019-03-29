### STAGE 1: Build ###
FROM node:8.12.0 as build

LABEL author="Benny Hwang"

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY package.json /usr/src/app/package.json
RUN npm install
RUN npm install react-scripts -g
COPY . /usr/src/app

WORKDIR frontend
RUN npm install

EXPOSE 3000
RUN npm run build

### STAGE 2: Production Environment ###
FROM nginx:1.14.2-alpine
COPY --from=build /usr/src/app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]