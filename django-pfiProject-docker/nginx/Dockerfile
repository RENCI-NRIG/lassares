FROM node:12.8.1-alpine AS build

WORKDIR /app

COPY quasar/package.json quasar/yarn.lock /app/
RUN yarn global add @quasar/cli

COPY quasar /app
RUN yarn
RUN quasar build

FROM nginx:alpine

COPY nginx/pfiProject_nginx_ssl.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/spa /dist/

CMD ["nginx", "-g", "daemon off;"]
