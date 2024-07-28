FROM node:18.16.0 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm config set proxy http://proxy.example.com:port && \
    npm config set https-proxy https://proxy.example.com:port
RUN npm install
RUN npm cache clean --force
COPY . .
RUN npm run build:prod

FROM nginx:stable-alpine as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
