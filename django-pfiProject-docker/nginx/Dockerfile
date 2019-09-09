FROM node:12.8.1-alpine AS build

WORKDIR /app

COPY vuejs/package.json vuejs/package-lock.json /app/
RUN npm install
RUN npm install @vue/cli@3.7.0 -g

COPY vuejs /app
RUN npm run build

FROM nginx:alpine

COPY nginx/pfiProject_nginx_ssl.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/ /dist/

CMD ["nginx", "-g", "daemon off;"]
