# develop stage
FROM node:12.8.1-alpine as dev 
WORKDIR /app
COPY quasar/package*.json ./
RUN yarn global add @quasar/cli
COPY . .
