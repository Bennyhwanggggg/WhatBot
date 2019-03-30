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
RUN npm install

EXPOSE 3000
RUN npm run build

### STAGE 2: Production Environment ###
FROM nginx:1.14.2-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /usr/src/app/build /usr/share/nginx/html
EXPOSE 80

CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'